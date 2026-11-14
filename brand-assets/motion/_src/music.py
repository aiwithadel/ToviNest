"""Procedurally generated, royalty-free light music bed (soft pad + pluck arpeggio + bass + shaker).
Original audio synthesized from code, so there is nothing to license.
python3 music.py <seconds> <out.wav> [variant]
"""
import sys, wave
import numpy as np

SR = 48000

def note(n):  # MIDI -> Hz
    return 440.0 * 2 ** ((n - 69) / 12)

def env_adsr(n, a, r):
    e = np.ones(n)
    ai, ri = int(a * SR), int(r * SR)
    e[:ai] = np.linspace(0, 1, ai) if ai else 1
    if ri:
        e[-ri:] *= np.linspace(1, 0, ri)
    return e

def pluck(f, dur, amp):
    t = np.arange(int(dur * SR)) / SR
    y = np.sin(2*np.pi*f*t) + .35*np.sin(4*np.pi*f*t) + .12*np.sin(6*np.pi*f*t)
    return amp * y * np.exp(-t / .32) * (1 - np.exp(-t / .004))

def pad(freqs, dur, amp):
    t = np.arange(int(dur * SR)) / SR
    y = np.zeros_like(t)
    for f in freqs:
        for k, g in [(1, 1), (2, .25), (3, .08)]:
            y += g * np.sin(2*np.pi*f*k*t + np.sin(2*np.pi*.3*t) * .4)
    return amp * y / len(freqs) * env_adsr(len(t), .6, .9)

def build(seconds, variant=0):
    bpm = [92, 96, 88][variant % 3]
    key = [60, 62, 57][variant % 3]          # C, D, A
    beat = 60 / bpm
    bar = 4 * beat
    prog = [(0, [0, 4, 7]), (7, [7, 11, 14]), (9, [9, 12, 16]), (5, [5, 9, 12])]   # I V vi IV
    n = int((seconds + 2) * SR)
    L, R = np.zeros(n), np.zeros(n)
    rng = np.random.default_rng(variant + 7)
    nbars = int(np.ceil(seconds / bar)) + 1
    for b in range(nbars):
        root, tri = prog[b % 4]
        t0 = b * bar
        i0 = int(t0 * SR)
        p = pad([note(key - 12 + x) for x in tri], bar + .8, .10)
        L[i0:i0+len(p)] += p[:max(0, n-i0)]; R[i0:i0+len(p)] += p[:max(0, n-i0)]
        for bb in (0, 2):  # bass
            s = pluck(note(key - 24 + root), beat * 1.8, .22)
            j = int((t0 + bb*beat) * SR); L[j:j+len(s)] += s[:max(0, n-j)]; R[j:j+len(s)] += s[:max(0, n-j)]
        arp = [tri[0], tri[1], tri[2], tri[1] + 12, tri[2], tri[1], tri[0] + 12, tri[2]]
        for k in range(8):  # eighth-note arpeggio, gently panned
            if b == 0 and k < 2:
                continue
            s = pluck(note(key + 12 + arp[k]), .9, .11 * (1 if k % 2 == 0 else .75))
            j = int((t0 + k*beat/2) * SR); pan = .5 + .3*np.sin(k)
            L[j:j+len(s)] += s[:max(0, n-j)] * (1-pan) * 1.4; R[j:j+len(s)] += s[:max(0, n-j)] * pan * 1.4
        for k in range(4):  # shaker on off-beats
            m = int(.06 * SR); sh = rng.standard_normal(m) * np.exp(-np.arange(m)/(.012*SR)) * .025
            sh = np.convolve(sh, [1, -1], 'same')
            j = int((t0 + k*beat + beat/2) * SR); L[j:j+m] += sh[:max(0, n-j)]; R[j:j+m] += sh[:max(0, n-j)] * .8
    # simple stereo echo for space
    for d, g in [(.23, .22), (.31, .16)]:
        k = int(d * SR)
        L[k:] += R[:-k] * g; R[k:] += L[:-k] * g
    n = int(seconds * SR)
    L, R = L[:n], R[:n]
    fade_in, fade_out = int(.4*SR), int(1.6*SR)
    for ch in (L, R):
        ch[:fade_in] *= np.linspace(0, 1, fade_in); ch[-fade_out:] *= np.linspace(1, 0, fade_out)**1.5
    peak = max(np.abs(L).max(), np.abs(R).max())
    g = 10 ** (-6 / 20) / peak       # peak at -6 dBFS: a light bed under voice / platform sounds
    return L * g, R * g

def write(path, L, R):
    data = (np.stack([L, R], 1) * 32767).astype(np.int16)
    with wave.open(path, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(data.tobytes())

if __name__ == "__main__":
    secs, out = float(sys.argv[1]), sys.argv[2]
    var = int(sys.argv[3]) if len(sys.argv) > 3 else 0
    write(out, *build(secs, var))
