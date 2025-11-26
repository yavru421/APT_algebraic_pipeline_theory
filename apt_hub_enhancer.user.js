// ==UserScript==
// @name         APT Hub Enhancer
// @namespace    http://your-namespace.com
// @version      1.0
// @description  Enhances the APT Hub with additional features like auto-copy, theme toggle, and local storage for pipelines.
// @author       John Dondlinger
// @match        https://apt-hub.tailscale.com/*
// @match        http://*.onion/*
// @grant        GM_setClipboard
// @grant        GM_getValue
// @grant        GM_setValue
// ==/UserScript==

(function () {
    'use strict';

    // Function to add copy buttons to tool outputs
    function addCopyButtons() {
        const outputs = document.querySelectorAll('.tool-output');
        outputs.forEach(output => {
            if (!output.querySelector('.copy-btn')) {
                const copyBtn = document.createElement('button');
                copyBtn.textContent = 'Copy Output';
                copyBtn.className = 'copy-btn';
                copyBtn.style.marginTop = '10px';
                copyBtn.style.padding = '5px 10px';
                copyBtn.style.background = 'var(--emerald)';
                copyBtn.style.color = 'var(--onyx)';
                copyBtn.style.border = 'none';
                copyBtn.style.borderRadius = '5px';
                copyBtn.style.cursor = 'pointer';
                copyBtn.onclick = () => {
                    GM_setClipboard(output.textContent);
                    alert('Output copied to clipboard!');
                };
                output.appendChild(copyBtn);
            }
        });
    }

    // Function to toggle dark/light theme
    function addThemeToggle() {
        const toggleBtn = document.createElement('button');
        toggleBtn.textContent = 'Toggle Theme';
        toggleBtn.style.position = 'fixed';
        toggleBtn.style.top = '20px';
        toggleBtn.style.right = '20px';
        toggleBtn.style.padding = '10px';
        toggleBtn.style.background = 'var(--gold)';
        toggleBtn.style.color = 'var(--deep-purple)';
        toggleBtn.style.border = 'none';
        toggleBtn.style.borderRadius = '50%';
        toggleBtn.style.cursor = 'pointer';
        toggleBtn.style.zIndex = '1000';

        let isDark = true;
        toggleBtn.onclick = () => {
            isDark = !isDark;
            document.body.style.filter = isDark ? 'none' : 'invert(1)';
            GM_setValue('theme', isDark ? 'dark' : 'light');
        };

        // Load saved theme
        const savedTheme = GM_getValue('theme', 'dark');
        if (savedTheme === 'light') {
            document.body.style.filter = 'invert(1)';
            isDark = false;
        }

        document.body.appendChild(toggleBtn);
    }

    // Function to save/load pipelines locally
    function enhancePipelineBuilder() {
        const form = document.querySelector('#pipeline-modules').closest('form');
        if (form) {
            const saveBtn = document.createElement('button');
            saveBtn.textContent = 'Save Pipeline';
            saveBtn.type = 'button';
            saveBtn.style.marginTop = '10px';
            saveBtn.onclick = () => {
                const name = document.getElementById('pipeline-name').value;
                const modules = Array.from(document.getElementById('pipeline-modules').selectedOptions).map(o => o.value);
                if (name && modules.length) {
                    const pipelines = GM_getValue('pipelines', {});
                    pipelines[name] = modules;
                    GM_setValue('pipelines', pipelines);
                    alert(`Pipeline "${name}" saved!`);
                }
            };
            form.appendChild(saveBtn);

            const loadSelect = document.createElement('select');
            loadSelect.innerHTML = '<option value="">Load Saved Pipeline</option>';
            const pipelines = GM_getValue('pipelines', {});
            Object.keys(pipelines).forEach(name => {
                const option = document.createElement('option');
                option.value = name;
                option.textContent = name;
                loadSelect.appendChild(option);
            });
            loadSelect.onchange = () => {
                const name = loadSelect.value;
                if (name) {
                    const modules = pipelines[name];
                    const select = document.getElementById('pipeline-modules');
                    Array.from(select.options).forEach(opt => opt.selected = modules.includes(opt.value));
                    document.getElementById('pipeline-name').value = name;
                }
            };
            form.appendChild(loadSelect);
        }
    }

    // Run enhancements on page load
    window.addEventListener('load', () => {
        addCopyButtons();
        addThemeToggle();
        enhancePipelineBuilder();
    });
})();