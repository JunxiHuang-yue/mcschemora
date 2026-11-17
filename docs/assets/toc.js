const toc = document.querySelector('.md-sidebar--secondary [data-md-component="toc"]');

if (toc) {
  const links = [...toc.querySelectorAll('a[href^="#"]')];
  const headings = links.map(link => document.getElementById(decodeURIComponent(link.hash.slice(1))));

  function updateToc() {
    const page = document.documentElement;
    const header = document.querySelector('.md-header');
    const threshold = (header?.getBoundingClientRect().bottom ?? 0) + 24;
    const atEnd = page.scrollHeight > window.innerHeight &&
      window.scrollY + window.innerHeight >= page.scrollHeight - 2;
    let selected = atEnd ? links.length - 1 : -1;

    if (!atEnd) {
      for (let index = 0; index < headings.length; index++) {
        if (headings[index]?.getBoundingClientRect().top <= threshold) selected = index;
      }
    }

    links.forEach((link, index) => {
      link.classList.toggle('md-nav__link--active', index === selected);
      if (index === selected) link.setAttribute('aria-current', 'location');
      else link.removeAttribute('aria-current');
    });
  }

  const schedule = () => window.requestAnimationFrame(updateToc);
  window.addEventListener('scroll', schedule, { passive: true });
  window.addEventListener('resize', schedule);
  window.addEventListener('load', schedule);
  window.addEventListener('hashchange', schedule);
  schedule();
}
