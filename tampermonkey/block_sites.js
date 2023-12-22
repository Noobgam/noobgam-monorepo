// ==UserScript==
// @name         Block sites
// @namespace    http://tampermonkey.net/
// @version      0.6
// @description  Block sites
// @author       Noobgam
// @match        http*://www.youtube.com/*
// @match        http*://www.quora.com/*
// @match        http*://www.youtu.be/*
// @grant        GM_addStyle
// @require      https://code.jquery.com/jquery-3.7.1.min.js
// @run-at       document-start
// ==/UserScript==

// I'm fucking retarded, ain't I?

function stopYoutubeWindow() {
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
}

function handleYoutube() {
    deleteShorts();
    stopYoutubeWindow();
}

function youtubeInject() {
    setInterval(handleYoutube, 200)
}

(function() {
    'use strict';
    handleYoutube();
    youtubeInject();
})();
