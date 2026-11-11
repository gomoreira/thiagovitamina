/* PostHog: pageviews, scroll depth, session replay, heatmaps and the portfolio funnel events. */
!function(t,e){var o,n,p,r;e.__SV||(window.posthog=e,e._i=[],e.init=function(i,s,a){function g(t,e){var o=e.split(".");2==o.length&&(t=t[o[0]],e=o[1]),t[e]=function(){t.push([e].concat(Array.prototype.slice.call(arguments,0)))}}(p=t.createElement("script")).type="text/javascript",p.crossOrigin="anonymous",p.async=!0,p.src=s.api_host.replace(".i.posthog.com","-assets.i.posthog.com")+"/static/array.js",(r=t.getElementsByTagName("script")[0]).parentNode.insertBefore(p,r);var u=e;for(void 0!==a?u=e[a]=[]:a="posthog",u.people=u.people||[],u.toString=function(t){var e="posthog";return"posthog"!==a&&(e+="."+a),t||(e+=" (stub)"),e},u.people.toString=function(){return u.toString(1)+".people (stub)"},o="init capture register register_once unregister identify alias set_config reset opt_in_capturing opt_out_capturing has_opted_out_capturing people.set people.set_once".split(" "),n=0;n<o.length;n++)g(u,o[n]);e._i.push([i,s,a])},e.__SV=1)}(document,window.posthog||[]);

var CONSENT_KEY = 'tv-consent';
var consent = null;
try { consent = localStorage.getItem(CONSENT_KEY); } catch (e) {}

// Until someone says yes, nothing is stored in the browser and nothing is recorded.
posthog.init('phc_q2kGD4TfbdLA6zzstSbBVcRtp5Qr8uwdBPFoNBWywmHv', {
  api_host: 'https://us.i.posthog.com',
  ui_host: 'https://us.posthog.com',
  person_profiles: 'identified_only',
  persistence: consent === 'yes' ? 'localStorage+cookie' : 'memory',
  disable_session_recording: consent !== 'yes',
  capture_pageview: true,
  capture_pageleave: true,
  enable_heatmaps: true,
  session_recording: { maskAllInputs: true }
});

(function () {
  var page = location.pathname.replace(/\/$/, '') || '/';
  var track = function (name, props) { try { posthog.capture(name, Object.assign({ page: page }, props || {})); } catch (e) {} };

  // Tester links: thiagovitamina.com/?ref=name tags every event of that visit.
  var ref = new URLSearchParams(location.search).get('ref');
  if (ref) { try { posthog.register({ ref: ref }); } catch (e) {} }

  // Funnel steps: which sections were seen.
  var seen = {};
  var sections = [
    ['#work', 'selected_work'], ['.feature', 'bauhaus'], ['.alsolive', 'also_live'],
    ['#about', 'about'], ['nav.next', 'case_end']
  ];
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        var key = e.target.getAttribute('data-track-section');
        if (e.isIntersecting && !seen[key]) { seen[key] = 1; track('section_viewed', { section: key }); io.unobserve(e.target); }
      });
    }, { rootMargin: '-45% 0px -45% 0px' });
    document.addEventListener('DOMContentLoaded', function () {
      sections.forEach(function (s) {
        var el = document.querySelector(s[0]);
        if (el) { el.setAttribute('data-track-section', s[1]); io.observe(el); }
      });
    });
  }

  // The contact sits under the stacked pages, so it counts once the page is scrolled to the end.
  var onScroll = function () {
    if (!seen.contact && document.getElementById('contact') && innerHeight + scrollY >= document.documentElement.scrollHeight - 120) {
      seen.contact = 1; track('section_viewed', { section: 'contact' }); removeEventListener('scroll', onScroll);
    }
  };
  addEventListener('scroll', onScroll, { passive: true });

  var caseName = function (el) {
    var a = el.closest("article, section");
    var h = a && a.querySelector('h3');
    return h ? h.textContent.trim() : undefined;
  };

  // Clicks: cases, contact channels and the live sites.
  document.addEventListener('click', function (ev) {
    var el = ev.target.closest('a, button');
    if (!el) return;
    var href = el.getAttribute('href') || '';
    if (el.id === 'copy') return track('contact_clicked', { channel: 'email_copy' });
    if (/linkedin\.com/.test(href)) return track('contact_clicked', { channel: 'linkedin' });
    if (/cv\.pdf$/.test(href)) return track('cv_downloaded');
    if (/instagram\.com/.test(href)) return track('contact_clicked', { channel: 'instagram' });
    if (/^mailto:/.test(href)) return track('contact_clicked', { channel: 'email' });
    if (el.classList.contains('btn-ink') && /(trade-in|mir|sc4a|criaaa)/.test(href)) return track('case_opened', { case: caseName(el) || href.replace(/\.html.*$/, '') });
    if (/^https?:/.test(href) && href.indexOf(location.host) < 0) return track('external_site_opened', { url: href, project: caseName(el) });
  }, true);

  // Case and live-site videos that actually played.
  var played = {};
  document.addEventListener('play', function (ev) {
    var v = ev.target, name = caseName(v) || (v.currentSrc || '').split('/').pop();
    if (v.tagName === 'VIDEO' && !played[name]) { played[name] = 1; track('video_played', { project: name }); }
  }, true);

  // Cookie note: the site's ink drop asks once, after the visitor has scrolled past the hero.
  if (consent) return;
  var note = document.createElement('div');
  note.className = 'cnote';
  note.setAttribute('role', 'region');
  note.setAttribute('aria-label', 'Cookie');
  note.innerHTML =
    '<svg class="cnote-drop" viewBox="0 0 64 64" aria-hidden="true"><path/></svg>' +
    '<p>One small cookie, so I can see which work gets opened. Nothing is sold or shared.</p>' +
    '<div class="cnote-act">' +
      '<button type="button" class="btn-ink cnote-yes"><span>Sure</span></button>' +
      '<button type="button" class="btn-ink cnote-no"><span>No, thanks</span></button>' +
    '</div>';

  // The drop breathes, with the same motion as the favicon.
  var path = note.querySelector('.cnote-drop path'), raf = 0, t0 = performance.now();
  var still = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var drawDrop = function (t) {
    var N = 48, R = 26.5, p = [], d = '';
    for (var i = 0; i < N; i++) {
      var a = i / N * Math.PI * 2;
      var r = R * (1 + .085 * Math.sin(2 * a + t * .55) + .06 * Math.sin(3 * a - t * .8 + 1.3) + .035 * Math.sin(5 * a + t * 1.25 + .4) + .02 * Math.sin(7 * a - t * 1.7));
      p[i] = [32 + Math.cos(a) * r + .8 * Math.sin(t * .4), 32 + Math.sin(a) * r * .94 + .6 * Math.cos(t * .33)];
    }
    for (var j = 0; j < N; j++) {
      var q = p[j], n = p[(j + 1) % N], m = [(q[0] + n[0]) / 2, (q[1] + n[1]) / 2];
      if (j === 0) { var z = p[N - 1]; d += 'M' + ((z[0] + q[0]) / 2).toFixed(2) + ' ' + ((z[1] + q[1]) / 2).toFixed(2); }
      d += 'Q' + q[0].toFixed(2) + ' ' + q[1].toFixed(2) + ' ' + m[0].toFixed(2) + ' ' + m[1].toFixed(2);
    }
    path.setAttribute('d', d + 'Z');
  };
  var loop = function (now) { drawDrop((now - t0) / 1000); raf = requestAnimationFrame(loop); };

  // Ink starts where the cursor enters, like Read the case.
  [].forEach.call(note.querySelectorAll('.btn-ink'), function (b) {
    var set = function (e) {
      var r = b.getBoundingClientRect();
      b.style.setProperty('--x', (e.clientX - r.left) + 'px');
      b.style.setProperty('--y', (e.clientY - r.top) + 'px');
      b.style.setProperty('--k', Math.ceil(Math.hypot(r.width, r.height) / 8));
    };
    b.addEventListener('pointerenter', set);
    b.addEventListener('pointerdown', set);
  });

  var close = function (answer) {
    try { localStorage.setItem(CONSENT_KEY, answer); } catch (e) {}
    if (answer === 'yes') {
      try { posthog.set_config({ persistence: 'localStorage+cookie' }); posthog.startSessionRecording(); } catch (e) {}
      note.querySelector('p').textContent = 'Thanks. Enjoy the work.';
    }
    track('cookie_answered', { answer: answer });
    note.classList.add('is-out', answer === 'yes' ? 'is-yes' : 'is-no');
    document.documentElement.style.scrollPaddingBottom = '';
    setTimeout(function () { cancelAnimationFrame(raf); removeEventListener('scroll', onTone); note.remove(); }, answer === 'yes' ? 1500 : 700);
  };
  note.querySelector('.cnote-yes').addEventListener('click', function () { close('yes'); });
  note.querySelector('.cnote-no').addEventListener('click', function () { close('no'); });

  // Over the black sections the glass turns dark, like the header.
  var tone = 0;
  var setTone = function () {
    tone = 0;
    var r = note.getBoundingClientRect(), els = document.elementsFromPoint(r.left + r.width / 2, r.top + r.height / 2);
    for (var i = 0; i < els.length; i++) {
      if (note.contains(els[i])) continue;
      note.classList.toggle('on-dark', !!els[i].closest('.dark,.contact'));
      break;
    }
  };
  var onTone = function () { if (!tone) tone = requestAnimationFrame(setTone); };

  var shown = false;
  var show = function () {
    if (shown) return; shown = true;
    document.body.appendChild(note);
    // Keyboard focus never lands under the note: the page keeps the note's height free when it scrolls to a focused element.
    document.documentElement.style.scrollPaddingBottom = (note.offsetHeight + 24) + 'px';
    drawDrop(0);
    setTone();
    addEventListener('scroll', onTone, { passive: true });
    addEventListener('resize', onTone);
    if (!still) raf = requestAnimationFrame(loop);
    requestAnimationFrame(function () { requestAnimationFrame(function () { note.classList.add('is-in'); }); });
  };
  var hero = null;
  var check = function () { if (scrollY > hero.offsetHeight * 0.6) { show(); removeEventListener('scroll', check); } };
  document.addEventListener('DOMContentLoaded', function () {
    hero = document.getElementById('hero');
    if (!hero) setTimeout(show, 1200); else addEventListener('scroll', check, { passive: true });
  });
})();
