/* 全站交互：主题切换、站内搜索、目录高亮、阅读进度 */
(function () {
  "use strict";

  /* ---------- 主题 ---------- */
  var root = document.documentElement;
  var saved = null;
  try { saved = localStorage.getItem("fsn-theme"); } catch (e) {}
  var qs = new URLSearchParams(window.location.search).get("theme");
  if (qs === "dark" || qs === "light") saved = qs;
  if (!saved) {
    saved = window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  }
  root.setAttribute("data-theme", saved);

  var themeBtn = document.getElementById("theme-btn");
  if (themeBtn) {
    var paint = function (t) {
      themeBtn.textContent = t === "dark" ? "☀" : "◐";
      themeBtn.title = t === "dark" ? "切换到浅色" : "切换到深色";
    };
    paint(saved);
    themeBtn.addEventListener("click", function () {
      var next = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
      root.setAttribute("data-theme", next);
      paint(next);
      try { localStorage.setItem("fsn-theme", next); } catch (e) {}
    });
  }

  /* ---------- 移动端侧栏开关 ---------- */
  var sidebar = document.getElementById("sidebar");
  var actions = document.querySelector(".topbar-actions");
  if (sidebar && actions && window.matchMedia("(max-width: 900px)").matches) {
    var btn = document.createElement("button");
    btn.className = "icon-btn";
    btn.textContent = "☰";
    btn.title = "目录";
    btn.addEventListener("click", function () { sidebar.classList.toggle("open"); });
    actions.insertBefore(btn, actions.firstChild);
  }

  /* ---------- 阅读进度 ---------- */
  var bar = document.getElementById("progress");
  if (bar) {
    var onScroll = function () {
      var h = document.documentElement.scrollHeight - window.innerHeight;
      bar.style.width = (h > 0 ? Math.min(100, (window.scrollY / h) * 100) : 0) + "%";
    };
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
  }

  /* ---------- 右侧目录 scrollspy ---------- */
  var tocLinks = [].slice.call(document.querySelectorAll(".toc a"));
  if (tocLinks.length) {
    var map = {};
    tocLinks.forEach(function (a) {
      var id = decodeURIComponent(a.getAttribute("href").slice(1));
      map[id] = a;
    });
    var heads = [].slice.call(document.querySelectorAll(".md h2[id], .md h3[id]"));
    if (heads.length && "IntersectionObserver" in window) {
      var current = null;
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) {
          if (en.isIntersecting) {
            var a = map[en.target.id];
            if (a && a !== current) {
              if (current) current.classList.remove("active");
              a.classList.add("active");
              current = a;
            }
          }
        });
      }, { rootMargin: "-72px 0px -75% 0px", threshold: 0 });
      heads.forEach(function (h) { io.observe(h); });
    }
  }

  /* ---------- 站内搜索 ---------- */
  var input = document.getElementById("q");
  var box = document.getElementById("results");
  if (input && box && window.SEARCH_INDEX) {
    var INDEX = window.SEARCH_INDEX;
    var browse = document.getElementById("browse");
    var cards = document.querySelector(".cards");

    var esc = function (s) {
      return s.replace(/[&<>"]/g, function (c) {
        return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
      });
    };

    var render = function (q) {
      q = q.trim().toLowerCase();
      if (!q) {
        box.hidden = true;
        box.innerHTML = "";
        if (browse) browse.hidden = false;
        if (cards) cards.hidden = false;
        return;
      }
      var hits = [];
      for (var i = 0; i < INDEX.length && hits.length < 120; i++) {
        var it = INDEX[i];
        var hay = (it.t + " " + it.p + " " + it.d).toLowerCase();
        if (hay.indexOf(q) !== -1) hits.push(it);
      }
      if (browse) browse.hidden = true;
      if (cards) cards.hidden = true;
      box.hidden = false;

      if (!hits.length) {
        box.innerHTML = '<div class="results-head">没有匹配「' + esc(q) + '」的笔记</div>' +
          '<div class="empty">试试更短的关键词，比如 View、协程、Dagger、排序</div>';
        return;
      }

      var rows = hits.map(function (it) {
        var dir = it.p.split("/").slice(0, -1).join(" / ");
        return '<a class="result" href="' + encodeURI(it.p) + '">' +
          "<b>" + esc(it.t) + "</b>" +
          '<span class="result-path">' + esc(dir) + "</span></a>";
      }).join("");

      box.innerHTML = '<div class="results-head">找到 ' + hits.length +
        (hits.length >= 120 ? "+" : "") + ' 篇包含「' + esc(q) + "」的笔记</div>" +
        '<div class="results-list">' + rows + "</div>";
    };

    var timer = null;
    input.addEventListener("input", function () {
      clearTimeout(timer);
      var v = input.value;
      timer = setTimeout(function () { render(v); }, 90);
    });
    input.addEventListener("keydown", function (e) {
      if (e.key === "Escape") { input.value = ""; render(""); input.blur(); }
      if (e.key === "Enter") {
        var first = box.querySelector(".result");
        if (first) window.location.href = first.getAttribute("href");
      }
    });

    var pre = new URLSearchParams(window.location.search).get("q");
    if (pre) { input.value = pre; render(pre); }

    document.addEventListener("keydown", function (e) {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") {
        e.preventDefault();
        input.focus();
        input.select();
      }
    });
  }
})();
