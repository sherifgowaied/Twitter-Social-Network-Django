var cookieconsentSrc="//cdnjs.cloudflare.com/ajax/libs/cookieconsent2/3.1.1/cookieconsent.min.js";function loadPlugin(e,o){var n=document.createElement("script");n.onload=o,n.src=e,n.type="text/javascript",n.async="true";var i=document.getElementsByTagName("script")[0];i.parentNode.insertBefore(n,i)}function initCookieConsent(){try{window.cookieconsent.initialise({palette:{popup:{background:"#000"},button:{background:"#f1d600"}},content:{link:"More info",href:"https://codio.com/legal/privacy/"},elements:{messagelink:'<span id="cookieconsent:desc" class="cc-message">{{message}} <a aria-label="learn more about cookies" tabindex="0" class="cc-link" href="{{href}}" rel="noopener noreferrer nofollow" target="{{target}}">{{link}}</a></span>',dismiss:'<button aria-label="{{dismiss}} dismiss cookie message" role=button tabindex="0" class="cc-btn cc-dismiss" autofocus>{{dismiss}}</button>'},window:'<div aria-modal="true" tabindex="-1" role="dialog" aria-label="cookie consent" aria-describedby="cookieconsent:desc" class="cc-window {{classes}}">\x3c!--googleoff: all--\x3e{{children}}\x3c!--googleon: all--\x3e</div>'})}catch(e){console.log("init cookie consent error",e)}}function isVisible(e){return!!(e.offsetWidth||e.offsetHeight||e.getClientRects().length)}function selectTopElement(){for(var e=document.querySelectorAll("input, a:not(.cc-link)"),o=0;o<e.length;o++){var n=e[o];if(isVisible(n)){n.focus();break}}}function focusDismissBtn(){var e=document.querySelector(".cc-dismiss");e&&(e.focus(),e.addEventListener("click",function(){setTimeout(selectTopElement,100)}))}window.addEventListener("load",function(){setTimeout(focusDismissBtn,100)}),window.location===window.parent.location&&loadPlugin(cookieconsentSrc,initCookieConsent);