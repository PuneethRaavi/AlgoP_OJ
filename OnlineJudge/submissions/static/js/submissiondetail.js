document.addEventListener('DOMContentLoaded', function() {
    // --- Right Panel: Code Editor Controls ---
    const codeViewer = document.getElementById('code-viewer');
    const themeSelector = document.getElementById('theme-selector');
    const codeFontSizeSelector = document.getElementById('code-font-size-selector');
    let editor;

    if (codeViewer) {
        const language = codeViewer.dataset.language.toLowerCase();
        let mode = 'text/plain';
        if (language.includes('python')) mode = 'python';
        else if (language.includes('c++') || language.includes('cpp')) mode = 'text/x-c++src';
        else if (language.includes('java')) mode = 'text/x-java';
        else if (language.includes('javascript')) mode = 'javascript';

        const savedTheme = localStorage.getItem('submission_theme') || 'dracula';
        const savedCodeFontSize = localStorage.getItem('submission_code_fontSize') || '12px';
        themeSelector.value = savedTheme;
        codeFontSizeSelector.value = savedCodeFontSize;

        editor = CodeMirror.fromTextArea(codeViewer, {
            lineNumbers: true,
            mode: mode,
            theme: savedTheme,
            readOnly: true,
            lineWrapping: true,
        });

        const editorWrapper = editor.getWrapperElement();
        editorWrapper.style.fontSize = savedCodeFontSize;

        themeSelector.addEventListener('change', function() {
            const newTheme = this.value;
            editor.setOption('theme', newTheme);
            localStorage.setItem('submission_theme', newTheme);
        });

        codeFontSizeSelector.addEventListener('change', function() {
            const newSize = this.value;
            editorWrapper.style.fontSize = newSize;
            localStorage.setItem('submission_code_fontSize', newSize);
        });
    }

    // --- Left Panel: Problem Description & Test Case Controls ---
    const problemContent = document.getElementById('problem-content');
    const problemFontSizeSelector = document.getElementById('problem-font-size-selector');
    
    function applyProblemFontSize(size) {
        const proseBlock = problemContent.querySelector('.prose');
        const testCaseBlocks = problemContent.querySelectorAll('pre');
        
        if (proseBlock) {
            proseBlock.style.fontSize = size;
        }
        testCaseBlocks.forEach(pre => {
            pre.style.fontSize = size;
        });
    }

    const savedProblemFontSize = localStorage.getItem('problem_font_size') || '12px';
    problemFontSizeSelector.value = savedProblemFontSize;
    applyProblemFontSize(savedProblemFontSize);

    problemFontSizeSelector.addEventListener('change', function() {
        const newSize = this.value;
        applyProblemFontSize(newSize);
        localStorage.setItem('problem_font_size', newSize);
    });
});