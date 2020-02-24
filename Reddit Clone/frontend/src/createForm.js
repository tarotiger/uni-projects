// createForm.js creates the forms for logging in and signing up 
// by z5259931

import * as image from './encodeImage.js'

//========================== CREATE LOGIN FORM ==========================//

const createLoginForm = () => {
    // creates a login form 
    const loginForm = document.createElement("form");
    loginForm.classList.add("login-form");
    loginForm.id = "loginForm";

    const logo = document.createElement("h1");
    logo.className = "flex-center logo";
    logo.style.margin = "auto";
    logo.textContent = "Seddit";
    loginForm.appendChild(logo);

    // Creates heading for login 
    const logInHead = document.createElement("h1");
    logInHead.textContent = "Log In";
    logInHead.classList.add("form-header");
    loginForm.appendChild(logInHead);

    // creates a username heading 
    const usernameHead = document.createElement("p");
    usernameHead.textContent = "Username";
    usernameHead.classList.add("form-description");
    loginForm.appendChild(usernameHead);

    // creates input text field 
    const userName = document.createElement("input");
    userName.type = "text";
    userName.name = "username";
    userName.id = "username-login";
    userName.placeholder = "username";
    userName.required = true;
    loginForm.appendChild(userName);

    // creates a password heading 
    const passwordHead = document.createElement("p");
    passwordHead.textContent = "Password";
    passwordHead.classList.add("form-description");
    loginForm.appendChild(passwordHead);

    // creates a password field 
    const password = document.createElement("input");
    password.type = "password";
    password.name = "password";
    password.id = "password-login";
    password.placeholder = "password";
    password.required = true;
    loginForm.appendChild(password);

    //creates a submit button 
    const submitButton = document.createElement("input");
    submitButton.type = "submit";
    submitButton.id = "loginButton"
    submitButton.value = "Sign In";
    loginForm.appendChild(submitButton);

    const loginError = document.createElement("div");
    loginError.id = "login-error";
    loginError.style.fontSize = "10px";
    loginError.style.color = "red";
    loginForm.appendChild(loginError);

    return loginForm;
}

//========================== CREATE SIGNUP FORM ==========================//

const createSignUpForm = () => {
    // creates a sign up form 
    const signUpForm = document.createElement("form");
    signUpForm.classList.add("login-form");
    signUpForm.id = "signupForm";

    const logo = document.createElement("h1");
    logo.className = "flex-center logo";
    logo.style.margin = "auto";
    logo.textContent = "Seddit";
    signUpForm.appendChild(logo);

    // creates heading for sign up
    const signUpHead = document.createElement("h1");
    signUpHead.textContent = "Sign Up";
    signUpHead.classList.add("form-header");
    signUpForm.appendChild(signUpHead);

    // name input 
    const userFullName = document.createElement("input");
    userFullName.type = "text";
    userFullName.name = "name";
    userFullName.id = "fullname-signup";
    userFullName.placeholder = "full name";
    userFullName.required = true;
    signUpForm.appendChild(userFullName);

    // creates input text field 
    const username = document.createElement("input");
    username.type = "text";
    username.name = "username";
    username.id = "username-signup";
    username.placeholder = "username";
    username.required = true;
    signUpForm.appendChild(username);

    // creates a password field 
    const password = document.createElement("input");
    password.type = "password";
    password.name = "password";
    password.id = "password-signup";
    password.placeholder = "password";
    password.required = true;
    signUpForm.appendChild(password);

    const email = document.createElement("input");
    email.type = "email";
    email.name = "user-email";
    email.id = "email-signup";
    email.required = true;
    email.placeholder = "e-mail";
    signUpForm.appendChild(email);

    // creates a submit button 
    const submitButton = document.createElement("input");
    submitButton.type = "submit";
    submitButton.name = "signUp";
    submitButton.id = "signupButton"
    submitButton.value = "Sign Up";
    signUpForm.appendChild(submitButton);

    const signupError = document.createElement("div");
    signupError.id = "signup-error";
    signupError.style.fontSize = "10px";
    signupError.style.color = "red";
    signUpForm.appendChild(signupError);

    return signUpForm;
}

//========================== CREATE POST FORM ==========================//

const createPostForm = () => {
    // creates a post form 
    const postForm = document.createElement("form");
    postForm.classList.add("post-form");
    postForm.id = "postForm";

    // creates heading for post form
    const userPostHead = document.createElement("h1");
    userPostHead.textContent = "Create a post";
    userPostHead.classList.add("form-header");
    postForm.appendChild(userPostHead);

    // post title heading 
    const postpostFormImageHeader = document.createElement("p");
    postpostFormImageHeader.textContent = "Title";
    postpostFormImageHeader.classList.add("form-description");
    postForm.appendChild(postpostFormImageHeader);

    // title input 
    const postTitle = document.createElement("input");
    postTitle.type = "text";
    postTitle.name = "title";
    postTitle.id = "postForm-title";
    postTitle.placeholder = "title";
    postTitle.required = true;
    postForm.appendChild(postTitle);

    // subseddit heading 
    const subsedditHeader = document.createElement("p");
    subsedditHeader.textContent = "Subseddit";
    subsedditHeader.classList.add("form-description");
    postForm.appendChild(subsedditHeader);

    // subseddit input 
    const postSubseddit = document.createElement("input");
    postSubseddit.type = "text";
    postSubseddit.name = "subseddit";
    postSubseddit.id = "postForm-subseddit";
    postSubseddit.placeholder = "subseddit";
    postForm.appendChild(postSubseddit);

    // post text heading 
    const postTextHeader = document.createElement("p");
    postTextHeader.textContent = "Content";
    postTextHeader.classList.add("form-description");
    postForm.appendChild(postTextHeader);

    // post text input 
    const postText = document.createElement("textarea");
    postText.name = "postText";
    postText.classList.add("form-textarea");
    postText.placeholder = "Enter content here...";
    postText.required = true;
    postForm.appendChild(postText);

    // post image heading
    const postFormImageHeader = document.createElement("p");
    postFormImageHeader.textContent = "Upload image";
    postFormImageHeader.classList.add("form-description");
    postForm.appendChild(postFormImageHeader);

    // post image input
    const postFormImage = document.createElement("input");
    postFormImage.type = "file";
    postFormImage.name = "image-upload";
    postFormImage.id = "postForm-image";
    postFormImage.onchange = image.encode;
    postFormImage.accept = "image/png, image/jpeg";
    postForm.appendChild(postFormImage);

    // creates a submit button 
    const submitPost = document.createElement("input");
    submitPost.type = "submit";
    submitPost.name = "submit-post";
    submitPost.id = "post-submit";
    submitPost.value = "Submit Post";
    postForm.appendChild(submitPost);

    return postForm;
}

export { createLoginForm, createSignUpForm, createPostForm };