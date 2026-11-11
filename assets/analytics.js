/* PostHog: pageviews, scroll depth, session replay, heatmaps and the portfolio funnel events. */
!function(t,e){var o,n,p,r;e.__SV||(window.posthog=e,e._i=[],e.init=function(i,s,a){function g(t,e){var o=e.split(".");2==o.length&&(t=t[o[0]],e=o[1]),t[e]=function(){t.push([e].concat(Array.prototype.slice.call(arguments,0)))}}(p=t.createElement("script")).type="text/javascript",p.crossOrigin="anonymous",p.async=!0,p.src=s.api_host.replace(".i.posthog.com","-assets.i.posthog.com")+"/static/array.js",(r=t.getElementsByTagName("script")[0]).parentNode.insertBefore(p,r);var u=e;for(void 0!==a?u=e[a]=[]:a="posthog",u.people=u.people||[],u.toString=function(t){var e="posthog";return"posthog"!==a&&(e+="."+a),t||(e+=" (stub)"),e},u.people.toString=function(){return u.toString(1)+".people (stub)"},o="init capture register register_once unregister identify alias set_config reset opt_in_capturing opt_out_capturing has_opted_out_capturing people.set people.set_once".split(" "),n=0;n<o.length;n++)g(u,o[n]);e._i.push([i,s,a])},e.__SV=1)}(document,window.posthog||[]);

posthog.init('phc_q2kGD4TfbdLA6zzstSbBVcRtp5Qr8uwdBPFoNBWywmHv', {
  api_host: 'https://us.i.posthog.com',
  ui_host: 'https://us.posthog.com',
  person_profiles: 'identified_only',
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
    if (/instagram\.com/.test(href)) return track('contact_clicked', { channel: 'instagram' });
    if (/^mailto:/.test(href)) return track('contact_clicked', { channel: 'email' });
    if (el.classList.contains('btn-ink') && /trade-in/.test(href)) return track('case_opened', { case: caseName(el) || 'Allstate Trade-In' });
    if (/^https?:/.test(href) && href.indexOf(location.host) < 0) return track('external_site_opened', { url: href, project: caseName(el) });
  }, true);

  // Case and live-site videos that actually played.
  var played = {};
  document.addEventListener('play', function (ev) {
    var v = ev.target, name = caseName(v) || (v.currentSrc || '').split('/').pop();
    if (v.tagName === 'VIDEO' && !played[name]) { played[name] = 1; track('video_played', { project: name }); }
  }, true);
})();
