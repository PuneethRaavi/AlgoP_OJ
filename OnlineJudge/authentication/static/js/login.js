/**
 * Toggles the visibility of a password field and swaps the visibility of the associated 'eye' and 'eye-off' icons.
 * @param {string} fieldId - The ID of the password input field.
 */
function togglePasswordVisibility(fieldId) {
    const passwordField = document.getElementById(fieldId);
    if (!passwordField) {
        console.error(`Password field with id '${fieldId}' not found.`);
        return;
    }

    // Find the icons within the same parent container as the input
    const container = passwordField.parentElement;
    const eyeIcon = container.querySelector('.eye-icon');
    const eyeOffIcon = container.querySelector('.eye-off-icon');

    if (!eyeIcon || !eyeOffIcon) {
        console.error('Eye icons not found for the password field.');
        return;
    }

    // Toggle the input type between 'password' and 'text'
    const isPassword = passwordField.type === 'password';
    passwordField.type = isPassword ? 'text' : 'password';

    // Toggle which icon is hidden
    eyeIcon.classList.toggle('hidden', !isPassword);
    eyeOffIcon.classList.toggle('hidden', isPassword);
}
