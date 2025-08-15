document.addEventListener('DOMContentLoaded', function() {
  const codeTextArea = document.getElementById('id_code');
  const languageSelect = document.getElementById('id_language');
  const themeSelect = document.getElementById('id_theme');
  const fontSizeSelect = document.getElementById('id_fontSize'); // Get the new font size selector
  const inputField = document.getElementById('id_input') || document.querySelector('textarea[name="input"], input[name="input"]');

  if (!codeTextArea || !languageSelect) {
    console.warn("Code editor not initialized — id_code or id_language missing.");
    return;
  }

  // Boilerplates keyed by canonical language
  const boilerplates = {
    python: 'def main():\n    # Your code here\n    print("Hello, World!")\n\nif __name__ == "__main__":\n    main()',
    cpp: '#include <iostream>\nusing namespace std;\n\nint main() {\n    // Your code here\n    std::cout << "Hello, World!" << std::endl;\n    return 0;\n}',
    java: 'public class Main {\n    public static void main(String[] args) {\n        // Your code here\n        System.out.println("Hello, World!");\n    }\n}',
    javascript: '// Read input from stdin\nconst fs = require("fs");\nconst input = fs.readFileSync(0, "utf-8").trim().split("\\\\n");\n\nfunction solve() {\n    console.log("Hello, World!");\n}\n\nsolve();'
  };

  // Map canonical language -> CodeMirror mode
  const modeMap = {
    python: 'python',
    cpp: 'text/x-c++src',
    java: 'text/x-java',
    javascript: 'javascript'
  };

  // small helper to canonicalize a select option
  function detectLang(opt) {
    const v = (opt.value || '').toLowerCase();
    const t = (opt.text || '').toLowerCase();

    // Prefer value when meaningful
    if (v) {
      if (v.includes('js') || v.includes('javascript') || v.includes('node')) return 'javascript';
      if (v.includes('python') || v === 'py') return 'python';
      if (v.includes('c++') || v.includes('cpp') || v.includes('cxx')) return 'cpp';
      // ensure 'java' is not matched for 'javascript'
      if (v.includes('java') && !v.includes('javascript')) return 'java';
    }

    // fallback on option text, check javascript first to avoid substring bug
    if (t.includes('javascript')) return 'javascript';
    if (t.includes('python')) return 'python';
    if (t.includes('c++') || t.includes('cpp')) return 'cpp';
    if (t.includes('java') && !t.includes('javascript')) return 'java';

    return 'plain';
  }

  const userCodeStash = {};
  const inputStash = {};

  const editor = CodeMirror.fromTextArea(codeTextArea, {
    lineNumbers: true,
    mode: 'text/plain',
    theme: localStorage.getItem('codeMirrorTheme') || 'monokai',
    autoCloseBrackets: true,
    matchBrackets: true,
    indentUnit: 4,
    smartIndent: true,
    tabSize: 4,
    indentWithTabs: false
  });

  // --- NEW FONT SIZE LOGIC ---
  const editorWrapper = editor.getWrapperElement(); // This is the .CodeMirror element
  if (fontSizeSelect && editorWrapper) {
      // Function to apply the font size
      const applyFontSize = (size) => {
          editorWrapper.style.fontSize = size;
          localStorage.setItem('codeMirrorFontSize', size);
          editor.refresh(); // Redraw the editor to adjust for new size
      };

      // Set initial font size from localStorage or the dropdown's default value
      const savedSize = localStorage.getItem('codeMirrorFontSize') || fontSizeSelect.value;
      fontSizeSelect.value = savedSize;
      applyFontSize(savedSize);

      // Add event listener for changes
      fontSizeSelect.addEventListener('change', () => {
          applyFontSize(fontSizeSelect.value);
      });
  }
  // --- END NEW FONT SIZE LOGIC ---


  // Theme Selector
  if (themeSelect) {
    themeSelect.value = localStorage.getItem('codeMirrorTheme') || themeSelect.value;
    themeSelect.addEventListener('change', () => {
      editor.setOption('theme', themeSelect.value);
      localStorage.setItem('codeMirrorTheme', themeSelect.value);
    });
  }

  // Save initial content under the detected language key
  const initialOption = languageSelect.options[languageSelect.selectedIndex];
  const initialLang = detectLang(initialOption);
  userCodeStash[initialLang] = codeTextArea.value || '';
  if (inputField) inputStash[initialLang] = inputField.value || '';

  function updateEditor() {
    // persist previous
    const prev = localStorage.getItem('currentLanguageValue');
    if (prev) {
      userCodeStash[prev] = editor.getValue();
      if (inputField) inputStash[prev] = inputField.value;
    }

    const selected = languageSelect.options[languageSelect.selectedIndex];
    const lang = detectLang(selected);

    localStorage.setItem('currentLanguageValue', lang);
    localStorage.setItem('codeMirrorLanguage', lang);

    editor.setOption('mode', modeMap[lang] || 'text/plain');

    if (userCodeStash[lang] && userCodeStash[lang].trim() !== '') {
      editor.setValue(userCodeStash[lang]);
    } else if (boilerplates[lang]) {
      editor.setValue(boilerplates[lang]);
    } else {
      editor.setValue('');
    }

    if (inputField) {
      inputField.value = inputStash[lang] || '';
    }
  }

  languageSelect.addEventListener('change', updateEditor);
  updateEditor();

});