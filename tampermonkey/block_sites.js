// ==UserScript==
// @name         Block sites
// @namespace    http://tampermonkey.net/
// @version      0.12.1
// @description  Block sites
// @author       Noobgam
// @match        http*://www.youtube.com/*
// @match        http*://www.youtu.be/*
// @match        http*://www.wanikani.com/*
// @grant        GM_addStyle
// @run-at       document-start
// ==/UserScript==

function removeElementByQuery(query) {
    // Use document.querySelectorAll to handle the removals instead of jQuery
    let elements = document.querySelectorAll(query);
    elements.forEach(element => element.remove());
}

function deleteShorts() {
    // Handling YouTube Shorts and other distracting elements
    removeElementByQuery(`[title='Shorts']`);
    removeElementByQuery(`[tab-title='Shorts']`);
    removeElementByQuery(`[id='shorts-container']`);
    removeElementByQuery(`[id='reply-button-end']`);
    removeElementByQuery(`.ytd-commentbox`);
    removeElementByQuery(`.ytd-comments-header-renderer[id='simple-box']`);
    removeElementByQuery(`ytd-reel-shelf-renderer`);
    // kekw. Youtube you're so funny.
    removeElementByQuery(`ytd-rich-shelf-renderer`);
}

function handleWanikani() {
    // Remove quiz statistics from WaniKani
    removeElementByQuery(`.quiz-statistics`);
}

function handleYoutube() {
    deleteShorts()
}

function youtubeInject() {
    // Setting interval to handle YouTube repeatedly
    setInterval(handleYoutube, 200);
}

(function() {
    'use strict';
    const hostname = window.location.hostname;
    let handlefunc = undefined;
    if (hostname.endsWith("youtube.com") || hostname.endsWith("youtu.be")) {
        handlefunc = handleYoutube;
    } else if (hostname.endsWith("wanikani.com")) {
        handlefunc = handleWanikani;
    }
    if (handlefunc) {
        setInterval(handlefunc, 200);
    }
})();
