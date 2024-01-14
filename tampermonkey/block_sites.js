// ==UserScript==
// @name         Block sites
// @namespace    http://tampermonkey.net/
// @version      0.8
// @description  Block sites
// @author       Noobgam
// @match        http*://www.youtube.com/*
// @match        http*://www.youtu.be/*
// @match        http*://www.wanikani.com/*
// @grant        GM_addStyle
// @require      https://code.jquery.com/jquery-3.7.1.min.js
// @run-at       document-start
// ==/UserScript==

// I'm fucking retarded, ain't I?

function stopWindow() {
    let dt = new Date();
    if (dt.getHours() > 0 && dt.getHours() < 12) {
        window.stop();
    }
}

function removeElementByQuery(query) {
    // requires jquery
    let elements = $(query).get();
    if (elements.length > 0) {
        for (let element of elements) {
            element.remove();
        }
    }
}

function deleteShorts() {
    // youtube does not care about W3C, there are lots of elements with same id.

    // shorts are addictivie.
    removeElementByQuery(`[title='Shorts']`);
    removeElementByQuery(`[tab-title='Shorts']`);    
    removeElementByQuery(`[id='shorts-container']`);

    // comments are toxic and braindead.
    removeElementByQuery(`[id='reply-button-end']`);
    removeElementByQuery(`.ytd-commentbox`)
    removeElementByQuery(`.ytd-comments-header-renderer[id='simple-box']`)
    removeElementByQuery(`ytd-reel-shelf-renderer`)
}

function handleWanikani() {
    // this is an unnecessary distration
    removeElementByQuery(`.quiz-statistics`)
}

function handleYoutube() {
    deleteShorts();
    stopWindow();
}

function youtubeInject() {
    setInterval(handleYoutube, 200)
}

(function() {
    'use strict';
    const hostname = window.location.hostname;
    let handlefunc = undefined;
    if (hostname.endsWith("youtube.com") || hostname.endsWith("youtu.be")) {
        handlefunc = handleYoutube;
    } else if (hostname.endsWith("wanikani.com")) {
        handlefunc = handleWanikani
    }
    if (handlefunc) {
        handlefunc();
        setInterval(handlefunc, 200);
    }
})();
