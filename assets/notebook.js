const menu = document.querySelector('#menu-toggle');
const sidebar = document.querySelector('#sidebar');
function closeMenu() {
  sidebar.classList.remove('open');
  menu.setAttribute('aria-expanded', 'false');
  menu.textContent = '打开目录';
}
menu.addEventListener('click', () => {
  const open = sidebar.classList.toggle('open');
  menu.setAttribute('aria-expanded', String(open));
  menu.textContent = open ? '收起目录' : '打开目录';
});
document.addEventListener('keydown', event => {
  if (event.key === 'Escape' && sidebar.classList.contains('open')) {
    closeMenu(); menu.focus();
  }
});
sidebar.addEventListener('click', event => {
  if (event.target.closest('a') && window.innerWidth <= 760) closeMenu();
});
const groups = [...document.querySelectorAll('.subject')];
const originalOpen = groups.map(group => group.open);
document.querySelector('#topic-search').addEventListener('input', event => {
  const query = event.target.value.trim().toLocaleLowerCase();
  let count = 0;
  groups.forEach((group, i) => {
    const subjectMatch = group.querySelector('summary').textContent.toLocaleLowerCase().includes(query);
    let matches = 0;
    group.querySelectorAll('.topic-link').forEach(link => {
      const visible = !query || subjectMatch || link.textContent.toLocaleLowerCase().includes(query);
      link.hidden = !visible;
      if (visible) matches++;
    });
    group.hidden = !matches;
    group.open = query ? matches > 0 : originalOpen[i];
    count += matches;
  });
  document.querySelector('#search-empty').hidden = count > 0;
});
const tocLinks = [...document.querySelectorAll('.toc a[href^="#"]')];
const sections = tocLinks.map(link => document.getElementById(decodeURIComponent(link.hash.slice(1)))).filter(Boolean);
function updateToc() {
  const threshold = window.innerWidth <= 760 ? 110 : 100;
  let current = sections[0];
  for (const section of sections) {
    if (section.getBoundingClientRect().top <= threshold) current = section;
  }
  tocLinks.forEach(link => {
    const active = current && decodeURIComponent(link.hash.slice(1)) === current.id;
    link.classList.toggle('current', Boolean(active));
    if (active) link.setAttribute('aria-current', 'location'); else link.removeAttribute('aria-current');
  });
}
let scheduled = false;
window.addEventListener('scroll', () => {
  if (scheduled) return;
  scheduled = true;
  requestAnimationFrame(() => { updateToc(); scheduled = false; });
}, {passive: true});
updateToc();
