// Tovi Nest: mobile sticky add-to-cart (see sections/tovi-sticky-atc.liquid)
if (!customElements.get('tovi-sticky-atc')) {
  customElements.define(
    'tovi-sticky-atc',
    class ToviStickyAtc extends HTMLElement {
      connectedCallback() {
        this.mainButton = document.querySelector('.product__info-container product-form button[name="add"]');
        this.mainPrice = document.querySelector('.product__info-container [id^="price-"]');
        this.button = this.querySelector('[data-sticky-button]');
        this.price = this.querySelector('[data-sticky-price]');
        if (!this.mainButton) return;
        this.button.addEventListener('click', () => {
          if (this.mainButton.disabled) {
            this.mainButton.scrollIntoView({ behavior: 'smooth', block: 'center' });
            return;
          }
          this.mainButton.click();
        });
        this.observer = new IntersectionObserver(([entry]) => this.toggle(!entry.isIntersecting && entry.boundingClientRect.top < 0), {
          threshold: 0,
        });
        this.observer.observe(this.mainButton);
        if (this.mainPrice) {
          this.priceObserver = new MutationObserver(() => this.sync());
          this.priceObserver.observe(this.mainPrice, { childList: true, subtree: true, characterData: true });
        }
        this.buttonObserver = new MutationObserver(() => this.sync());
        this.buttonObserver.observe(this.mainButton, { attributes: true, childList: true, subtree: true });
        this.sync();
      }
      sync() {
        if (this.mainPrice) {
          const sale = this.mainPrice.querySelector('.price__sale .price-item--sale');
          const regular = this.mainPrice.querySelector('.price__regular .price-item--regular');
          const onSale = this.mainPrice.querySelector('.price--on-sale');
          const el = onSale && sale ? sale : regular;
          if (el) this.price.textContent = el.textContent.trim();
        }
        this.button.disabled = this.mainButton.disabled;
        this.button.textContent = this.mainButton.disabled ? this.mainButton.textContent.trim() : this.dataset.label;
      }
      toggle(show) {
        this.classList.toggle('is-visible', show);
        document.body.classList.toggle('tovi-has-sticky', show);
      }
      disconnectedCallback() {
        this.observer?.disconnect();
        this.priceObserver?.disconnect();
        this.buttonObserver?.disconnect();
        document.body.classList.remove('tovi-has-sticky');
      }
    }
  );
}
