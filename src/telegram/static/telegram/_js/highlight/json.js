import hljs from 'highlight.js/lib/core';
import json from 'highlight.js/lib/languages/json';
import 'highlight.js/styles/agate.min.css'; // Theme

hljs.safeMode()
hljs.registerLanguage('json', json);


document.querySelectorAll('pre > code.hljs.language-json').forEach(element => {
    hljs.highlightElement(element)
    element.style.fontSize = "1rem"
});
