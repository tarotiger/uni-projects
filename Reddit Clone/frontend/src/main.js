/**
 * Written by A. Hinds with Z. Afzal 2018 for UNSW CSE.
 * 
 * Updated 2019.
 */

// import your own scripts here.

import * as createForm from './createForm.js';

// your app must take an apiUrl as an argument --
// this will allow us to verify your apps behaviour with 
// different datasets.
function initApp(apiUrl) {
  //==================== SEDDIT PAGE SETUP ====================//

  window.lastPost = 0;
  window.upvotes = 0;
  window.follows = [];
  window.subseddits = [];
  window.location.hash = "";

  //==================== GENERATES BANNER+ITEMS====================//

  const banner = createBanner();
  document.getElementById("root").appendChild(banner);

  const main = document.createElement("main");
  main.id = "content";
  document.getElementById("root").appendChild(main);

  main.appendChild(createFeedContainer());

  const userOptions = document.createElement("ul");
  userOptions.classList.add("nav");
  userOptions.id = "user-options"
  banner.appendChild(userOptions);

  const searchContainer = document.createElement("li");
  searchContainer.classList.add("nav-item");
  userOptions.appendChild(searchContainer);

  const sedditSearch = document.createElement("input");
  sedditSearch.dataset.idSearch = "";
  sedditSearch.type = "search";
  sedditSearch.placeholder = "Search Seddit";
  searchContainer.appendChild(sedditSearch);

  const loginContainer = document.createElement("li");
  loginContainer.classList.add("nav-item");
  userOptions.appendChild(loginContainer);

  const loginButton = createLoginButton();
  loginContainer.appendChild(loginButton);

  const signupContainer = document.createElement("li");
  signupContainer.classList.add("nav-item");
  userOptions.appendChild(signupContainer);

  const signupButton = createSignupButton();
  signupContainer.appendChild(signupButton);

  // generates a modal window for logging in
  const loginWindow = document.createElement("div");
  loginWindow.classList.add("modal");
  loginWindow.id = "login-window";
  document.getElementById("root").appendChild(loginWindow);

  const loginForm = createForm.createLoginForm();
  loginWindow.appendChild(loginForm);

  // generates a modal window for signup
  const signupWindow = document.createElement("div");
  signupWindow.classList.add("modal");
  signupWindow.id = "signup-window";
  document.getElementById("root").appendChild(signupWindow);

  const signUpForm = createForm.createSignUpForm();
  signupWindow.appendChild(signUpForm);

  //==================== END OF BANNER+ITEMS ===================//

  // modal window for which users upvoted
  const upvoteWindow = document.createElement("div");
  upvoteWindow.classList.add("modal");
  upvoteWindow.id = "upvote-window";
  document.getElementById("root").appendChild(upvoteWindow);

  // contains the users who upvoted a post
  const upvoteContent = document.createElement("div");
  upvoteContent.id = "upvote-content";
  upvoteContent.classList.add("upvoted-user-window");
  upvoteWindow.appendChild(upvoteContent);

  // modal window for comments 
  const commentWindow = document.createElement("div");
  commentWindow.classList.add("modal");
  commentWindow.id = "comment-window";
  document.getElementById("root").appendChild(commentWindow);

  // modal window for creating posts
  const postWindow = document.createElement("div");
  postWindow.classList.add("modal");
  postWindow.id = "post-window";
  document.getElementById("root").appendChild(postWindow);

  // modal window for profile 
  const profileWindow = document.createElement("div");
  profileWindow.classList.add("modal");
  profileWindow.id = "profile-window";
  document.getElementById("root").appendChild(profileWindow);

  // create feed 
  createFeed(apiUrl);
  populateFeed(apiUrl, "/post/public");

  //====================END OF SETUP====================//

  // reveals the login form 
  document.getElementById("loginButton").addEventListener('click', () => {
    loginWindow.style.display = "inline-block";
  });

  // reveals the sign up form 
  document.getElementById("signupButton").addEventListener('click', () => {
    signupWindow.style.display = "inline-block";
  })

  // exits from sign up and login form when the user clicks on the background 
  window.addEventListener('click', (event) => {
    if (event.target === loginWindow || event.target === signupWindow) {
      loginWindow.style.display = "none";
      signupWindow.style.display = "none";
      loginForm.reset();
      signUpForm.reset();
    } else if (event.target === document.getElementById("upvote-window")) {
      while (upvoteContent.firstChild) {
        upvoteContent.removeChild(upvoteContent.firstChild);
      }
      event.target.style.display = "none";
    } else if (event.target === document.getElementById("comment-window")) {
      event.target.style.display = "none";
      document.getElementById("comment-content").remove();
    } else if (event.target === document.getElementById("post-window")) {
      event.target.style.display = "none";
    } else if (event.target === document.getElementById("profile-window")) {
      event.target.style.display = "none";
      document.getElementsByClassName("profile-container")[0].remove();
    }
  });

  // submits an authentication to the backend server (auth/login)
  loginForm.onsubmit = (e) => {
    e.preventDefault();
    login(apiUrl);
  }

  // submits an authentication to the backend server (auth/signup)
  signUpForm.onsubmit = (e) => {
    e.preventDefault();
    signup(apiUrl);
  }

  // allows infinite scrolling for user feed
  window.addEventListener('scroll', (e) => {
    if (document.getElementById("feed-user") != null) {
      if (document.getElementById("feed-user").classList.contains("active")) {
        loadMore(e, apiUrl);
      }
    }
  });

  sedditSearch.addEventListener('keypress', (e) => {
    // 13 is the keycode for enter 
    if (e.keyCode === 13 && window.token != null) {
      window.queries = 0;
      refreshFeed(apiUrl);
      searchSeddit(apiUrl, sedditSearch.value);
      sedditSearch.value = "";
    }
  })
}

// will go through each user you have followed and search their posts 
const searchSeddit = (apiUrl, query) => {
  // displays the number of results found
  const numQueries = document.createElement("div");
  numQueries.style.padding = "5px 0px";
  numQueries.textContent = `${window.queries} result/s found with query '${query}'`;
  document.getElementById("feed").appendChild(numQueries);

  // goes through each user that you're following and returns the posts they have made 
  window.follows.forEach(element => {
    fetch(`${apiUrl}/user/?username=${element}`, {
        headers: {
          'Authorization': `Token ${window.token}`
        }
      })
      .then((response) => response.json())
      .then((user) => {
        console.log(user);
        matchQuery(user, apiUrl, query, numQueries);
      })
  });
}

// checks if title and text match the query of the user 
const matchQuery = (user, apiUrl, query, numQueries) => {
  user.posts.forEach(postId => {
    fetch(`${apiUrl}/post/?id=${postId}`, {
        headers: {
          'Authorization': `Token ${window.token}`
        }
      })
      .then((response) => response.json())
      .then((post) => {
        // if post title or text includes query load the post 
        if (post.text.includes(query) || post.title.includes(query)) {
          createPost(post, apiUrl, document.getElementById("feed"));
          window.queries++;
          numQueries.textContent = `${window.queries} result/s found with query '${query}'`;
        }
      })
  });
}

// creaqtes a drop down menu for subseddits 
const createDropDown = (apiUrl) => {
  const subsedditContainer = document.createElement("div");
  subsedditContainer.id = "subseddit-container";
  subsedditContainer.classList.add("subseddit-container");

  const currentSubseddit = document.createElement("div");
  currentSubseddit.textContent = "s/all";
  currentSubseddit.classList.add("current-subseddit");

  const subsedditChoices = document.createElement("div");
  subsedditChoices.id = "subseddit-choices";
  subsedditChoices.classList.add("subseddit-choices");

  // when container is clicked display the dropdown box
  subsedditContainer.addEventListener('click', () => {
    if (subsedditChoices.style.display !== "block") {
      subsedditChoices.style.display = "block";
    } else {
      subsedditChoices.style.display = "none";
    }
  })

  // inserts the drop down box after logo 
  document.getElementById("nav").insertBefore(subsedditContainer, document.getElementById("user-options"));
  subsedditContainer.appendChild(currentSubseddit);
  subsedditContainer.appendChild(subsedditChoices);

  window.subseddits.forEach((element) => {
    const subseddit = document.createElement("a");
    subseddit.href = `#s/${element}`;
    subseddit.textContent = `s/${element}`;
    subseddit.addEventListener('click', () => {
      loadSubseddit(apiUrl, element);
      currentSubseddit.textContent = `s/${element}`
    })
    subsedditChoices.appendChild(subseddit);
  });
}

// loads the subseddit by checking if each post is made in the subseddit
const loadSubseddit = (apiUrl, subseddit) => {
  refreshFeed(apiUrl);

  parent = document.getElementById("feed");
  createLoading(parent);
  fetch(`${apiUrl}/user/feed`, {
      headers: {
        'Authorization': 'Token ' + window.token
      }
    })
    .then((response) => {
      return response.json();
    })
    .then((postObject) => {
      for (const posts in postObject.posts) {
        if (postObject.posts[posts].meta.subseddit === subseddit) {
          createPost(postObject.posts[posts], apiUrl, parent);
        }
      }
      removeLoading();
    })
}

// deletes the dropdown element
const removeDropDown = () => {
  if (document.getElementById("subseddit-container") != null) {
    document.getElementById("subseddit-container").remove();
  }
}

// produces a new feed and interface when user logs in 
const login = (apiUrl) => {
  const usernameLogin = document.getElementById("username-login").value;
  const passwordLogin = document.getElementById("password-login").value;

  fetch(`${apiUrl}/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        username: usernameLogin,
        password: passwordLogin
      })
    })
    .then((response) => {
      document.getElementById("loginForm").reset();

      if (response.status === 200) {
        // login and signup button and replaces it with a profile button
        document.getElementById("login-window").style.display = "none";
        document.getElementById("signupButton").remove();
        document.getElementById("loginButton").remove();
        const profileButton = createProfileButton(apiUrl);
        document.getElementById("user-options").appendChild(profileButton);
        createLogoutDiv();
        return response.json();
      } else if (response.status === 403) {
        document.getElementById("login-error").textContent = "Invalid username/password";
        return new Error(response.status);
      }
    })
    .then((token) => {
      // prevents page from refreshing if token is not returned from API
      if (typeof token.token !== 'undefined') {
        window.token = token.token;
        getUserId(apiUrl);
        getFollowers(apiUrl);
        // refreshes the interface 
        refreshFeed(apiUrl);
        populateFeed(apiUrl, "/post/public");
        document.getElementById("feed-public").click();
      }
    })
    .catch((error) => console.log(error));
}

// produces a new feed and interface when user signs up
const signup = (apiUrl) => {
  const usernameSignup = document.getElementById("username-signup").value;
  const passwordSignup = document.getElementById("password-signup").value;
  const emailSignup = document.getElementById("email-signup").value;
  const fullname = document.getElementById("fullname-signup").value;

  fetch(`${apiUrl}/auth/signup`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        username: usernameSignup,
        password: passwordSignup,
        email: emailSignup,
        name: fullname
      })
    })
    .then((response) => {
      document.getElementById("signupForm").reset();

      if (response.status === 200) {
        document.getElementById("signup-window").style.display = "none";
        document.getElementById("signupButton").remove();
        document.getElementById("loginButton").remove();
        const profileButton = createProfileButton(apiUrl);
        document.getElementById("user-options").appendChild(profileButton);
        createLogoutDiv();
        return response.json();
      } else if (response.status === 403) {
        document.getElementById("signup-error").textContent = "Invalid username/password";
        throw new Error(response.status);
      } else if (response.status === 409) {
        document.getElementById("signup-error").textContent = "Username is taken";
        throw new Error(response.status);
      }
    })
    .then((token) => {
      window.token = token.token;
      getUserId(apiUrl);
      getFollowers(apiUrl);
      // refreshes interface 
      refreshFeed(apiUrl);
      populateFeed(apiUrl, "/post/public");
      document.getElementById("feed-public").click();
    })
    .catch((error) => {
      console.log(error);
    })
}

// creates logout button
const createLogoutDiv = () => {
  const logout = document.createElement("li");
  logout.textContent = "(logout)";
  logout.classList.add("nav-item");
  logout.id = "logout";

  document.getElementById("user-options").appendChild(logout);

  // refreshes window to logout :P
  logout.addEventListener('click', () => {
    location.reload();
  })
}

const createLoginButton = () => {
  const loginButton = document.createElement("button");
  loginButton.dataset.idLogin = "";
  loginButton.id = "loginButton";
  loginButton.className = "button button-primary";
  loginButton.textContent = "Log In";

  return loginButton;
}

const createSignupButton = () => {
  const signupButton = document.createElement("button");
  signupButton.dataset.idSignup = "";
  signupButton.id = "signupButton";
  signupButton.className = "button button-secondary";
  signupButton.textContent = "Sign Up";

  return signupButton;
}

const createProfileButton = (apiUrl) => {
  const profileButton = document.createElement("button");
  profileButton.id = "profileButton";
  profileButton.className = "button button-primary";
  profileButton.textContent = "Profile";

  // displays user profile when clicked 
  profileButton.addEventListener('click', () => {
    document.getElementById("profile-window").style.display = "inline-block";
    generateOwnProfile(apiUrl, window.userId);
  })

  return profileButton;
}

// creates banner and appends logo
const createBanner = () => {
  const banner = document.createElement("header");
  banner.id = "nav";
  banner.classList.add("banner");

  const logo = document.createElement("h1");
  logo.className = "flex-center logo";
  logo.textContent = "Seddit";

  banner.appendChild(logo);

  return banner;
}

// provides the user the ability to post, switch between between user 
// and public feed 
const createFeed = (apiUrl) => {
  const feed = document.getElementById("feed");

  const feedHeader = document.createElement("div");
  feedHeader.classList.add("feed-header");

  const feedPublic = document.createElement("h3");
  feedPublic.classList.add("feed-title");
  feedPublic.classList.add("alt-text");
  feedPublic.id = "feed-public";
  feedPublic.classList.add("feed-title-selected");
  feedPublic.textContent = "Popular posts";

  // user is logged in if window.token != null
  if (window.token != null) {
    const feedUser = document.createElement("h3");
    feedUser.classList.add("feed-title");
    feedUser.classList.add("alt-text");
    feedUser.id = "feed-user";
    feedUser.textContent = "Your feed";
    feedHeader.appendChild(feedUser);

    feedUser.addEventListener('click', () => {
      loadUserFeed(apiUrl);
    })

    feedPublic.addEventListener('click', () => {
      loadPublicFeed(apiUrl);
    })
  }

  feed.appendChild(feedHeader);
  feedHeader.appendChild(feedPublic);

  // user is logged in if window.token != null
  if (window.token != null) {
    const postButton = document.createElement("button");
    postButton.className = "button button-secondary";
    postButton.id = "postButton";
    postButton.textContent = "Post";

    // creates a post form if there isn't one 
    if (document.getElementById("postForm") == null) {
      // window that contains uploading a post 
      const postForm = createForm.createPostForm();
      document.getElementById("post-window").appendChild(postForm);
    }

    postButton.addEventListener('click', () => {
      document.getElementById("post-window").style.display = "inline-block";
    })

    document.getElementById("postForm").onsubmit = (e) => {
      e.preventDefault();
      makePost(apiUrl);
    }

    feedHeader.appendChild(postButton);
  }

  return feed;
}

// creates a loading spinning circle
const createLoading = (parent) => {
  if (document.getElementById("loading") == null) {
    const loadingContainer = document.createElement("div");
    loadingContainer.id = "loading";
    loadingContainer.style.textAlign = "center";
    parent.appendChild(loadingContainer);

    const loading = document.createElement("div");
    loading.classList.add("loading-animation");
    loadingContainer.appendChild(loading);
  }
}

// removes the loading circle
const removeLoading = () => {
  if (document.getElementById("loading") != null) {
    document.getElementById("loading").remove();
  }
}

// populates the feed with either posts from public or user
const populateFeed = (apiUrl, feed) => {
  const parent = document.getElementById("feed");
  createLoading(document.getElementById("content"));

  // checks if user has logged in 
  if (feed === "/post/public") {
    populatePublic(apiUrl, parent);
  } else {
    populateUser(apiUrl, parent);
  }
}

// populates feed with posts from public
const populatePublic = (apiUrl, parent) => {
  fetch(`${apiUrl}/post/public`)
    .then((response) => {
      return response.json();
    })
    .then((postObject) => {
      console.log(postObject.posts);
      for (const posts in postObject.posts) {
        createPost(postObject.posts[posts], apiUrl, parent);
      }
      removeLoading();
    })
}

// populates feed with posts from users and creates a drop down menu
const populateUser = (apiUrl, parent) => {
  window.lastPost = 0;
  fetch(`${apiUrl}/user/feed`, {
      headers: {
        'Authorization': 'Token ' + window.token
      }
    })
    .then((response) => {
      return response.json();
    })
    .then((postObject) => {
      console.log(postObject.posts);
      if (postObject.posts.length === 0) {
        const message = document.createElement("h4");
        message.textContent = "Follow some users to start your feed";
        document.getElementById("feed").appendChild(message);
      }
      createUserFeed(postObject.posts, apiUrl, parent);
      removeLoading();
      // removes old dropdown menu for subseddit if it still exists
      if (document.getElementById("subseddit-container") != null) {
        document.getElementById("subseddit-container").remove();
      }
      createDropDown(apiUrl);
    })
}

// appends the post to the feeed
const createUserFeed = (posts, apiUrl, parent) => {
  for (const post in posts) {
    const userPostSubseddit = posts[post].meta.subseddit;
    // appends which subseddits user is subscribed to 
    if (!window.subseddits.includes(userPostSubseddit) && userPostSubseddit !== "all") {
      window.subseddits.push(posts[post].meta.subseddit);
    }
    createPost(posts[post], apiUrl, parent);
    // stores the last post id to allow infinite scrolling 
    window.lastPost++;
  }
}

// using data, createPost creates a seddit post and appends it to the parent
const createPost = (data, apiUrl, parent) => {
  const post = document.createElement("li");
  post.classList.add("post");
  post.dataset.idPost = "";

  const content = document.createElement("div");
  content.classList.add("content");

  const title = document.createElement("h4");
  title.dataset.idTitle = "";
  title.className = "post-title alt-text";
  title.textContent = data.title;

  const postText = document.createElement("p");
  const postTextNode = document.createTextNode(data.text);
  postText.classList.add("post-text");

  // converts unix time stamp from seconds to milliseconds
  const postDate = new Date(data.meta.published * 1000);
  const postDateText = `${postDate.getDate()}/${postDate.getMonth() + 1}/${postDate.getFullYear()}`;

  const author = document.createElement("p");
  const authorTextNode = document.createTextNode("Posted by @" + data.meta.author + " on " + postDateText);
  author.classList.add("post-author");
  author.dataset.idAuthor = "";

  author.addEventListener('click', () => {
    if (window.token != null) {
      if (data.meta.author !== window.username) {
        generateProfile(apiUrl, data.meta.author);
        document.getElementById("profile-window").style.display = "inline-block";
      }
    } else {
      document.getElementById("loginButton").click();
    }
  })

  // post thumbnail
  const thumbnail = document.createElement("img");
  thumbnail.src = "data:image/jpeg;base64," + data.image;
  thumbnail.classList.add("post-thumbnail");

  const upvotes = document.createElement("div");
  upvotes.classList.add("post-upvotes");

  const upvoteButton = document.createElement("div");
  upvoteButton.classList.add("post-upvote-button");
  upvoteButton.clicked = false;

  const upvoteButtonImg = document.createElement("img");
  upvoteButtonImg.src = "../images/upvote.png";

  if (window.token != null) {
    if (data.meta.upvotes.includes(window.userId)) {
      upvoteButton.style.backgroundColor = "#888";
      upvoteButton.clicked = true;
      window.upvotes++;
    }
  }

  upvoteButton.addEventListener('click', () => {
    if (window.token == null) {
      document.getElementById("loginButton").click();
    }
    if (upvoteButton.clicked === false) {
      upvotePost(apiUrl, data.id, upvoteContent, upvoteButton)
    } else if (upvoteButton.clicked === true) {
      deleteUpvote(apiUrl, data.id, upvoteContent, upvoteButton);
    }
  })

  // displays the number of upvotes a post has 
  const upvoteContent = createUpvoteContent(data);

  upvoteContent.addEventListener('click', () => {
    if (window.token == null) {
      document.getElementById("loginButton").click();
    } else {
      // fetches the users who have upvoted the post 
      fetch(`${apiUrl}/post/?id=${data.id}`, {
          headers: {
            'Authorization': `Token ${window.token}`
          }
        })
        .then((response) => response.json())
        .then((post) => {
          populateUpvotes(post.meta.upvotes, document.getElementById("upvote-content"), apiUrl);
          // reveals modal window
          document.getElementById("upvote-window").style.display = "inline-block";
        })
    }
  })

  const subseddit = document.createElement("div");
  subseddit.classList.add("post-subseddit");
  subseddit.textContent = "s/" + data.meta.subseddit;

  const comments = document.createElement("div");
  comments.classList.add("post-comments")
  comments.textContent = data.comments.length + " Comments";

  comments.addEventListener('click', () => {
    if (window.token == null) {
      document.getElementById("loginButton").click();
    } else {
      populateComments(data, document.getElementById("comment-window"), apiUrl);
      // reveals modal window
      document.getElementById("comment-window").style.display = "inline-block";
    }
  })

  parent.appendChild(post);
  post.appendChild(upvotes);
  upvotes.appendChild(upvoteButton);
  upvoteButton.appendChild(upvoteButtonImg);
  upvotes.appendChild(upvoteContent);
  post.appendChild(thumbnail);
  post.appendChild(content);
  content.appendChild(title);
  content.appendChild(postText);
  postText.appendChild(postTextNode);
  content.appendChild(subseddit);
  content.appendChild(author);
  author.appendChild(authorTextNode);
  content.appendChild(comments);

  // if you are the author of the post, allow the user to delete the post 
  if (data.meta.author === window.username) {
    const deletePostDiv = document.createElement("div");
    deletePostDiv.style.color = "red";
    deletePostDiv.style.fontSize = "8px";
    deletePostDiv.style.display = "inline-block";
    deletePostDiv.style.textDecoration = "underline";
    deletePostDiv.textContent = "delete";

    content.appendChild(deletePostDiv);

    deletePostDiv.addEventListener('click', () => {
      deletePost(apiUrl, data.id);
    })
  }
}


// deletes post by sending a request to the api 
const deletePost = (apiUrl, id) => {
  fetch(`${apiUrl}/post/?id=${id}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Token ${window.token}`
      }
    })
    .then((response) => response.json())
    .then((status) => {
      // refreshes the feed interface
      refreshFeed(apiUrl);
      populateFeed(apiUrl, "/post/public");
      populateComments(data, document.getElementById("comment-window"), apiUrl);
    })
}

// same as create post but without the interactivity 
// mainly for user profile
const createPostFake = (data, apiUrl, parent) => {
  const post = document.createElement("li");
  post.classList.add("post");
  post.dataset.idPost = "";

  const content = document.createElement("div");
  content.classList.add("content");

  const title = document.createElement("h4");
  title.dataset.idTitle = "";
  title.className = "post-title alt-text";
  title.textContent = data.title;

  const postText = document.createElement("p");
  const postTextNode = document.createTextNode(data.text);
  postText.classList.add("post-text");

  // converts unix time stamp from seconds to milliseconds
  const postDate = new Date(data.meta.published * 1000);
  const postDateText = `${postDate.getDate()}/${postDate.getMonth() + 1}/${postDate.getFullYear()}`;

  const author = document.createElement("p");
  const authorTextNode = document.createTextNode("Posted by @" + data.meta.author + " on " + postDateText);
  author.classList.add("post-author");
  author.dataset.idAuthor = "";

  const thumbnail = document.createElement("img");
  thumbnail.src = "data:image/jpeg;base64," + data.image;
  thumbnail.classList.add("post-thumbnail");

  const upvotes = document.createElement("div");
  upvotes.classList.add("post-upvotes");

  const upvoteButton = document.createElement("div");
  upvoteButton.classList.add("post-upvote-button");
  upvoteButton.clicked = false;

  const upvoteButtonImg = document.createElement("img");
  upvoteButtonImg.src = "../images/upvote.png";

  if (window.token != null) {
    if (data.meta.upvotes.includes(window.userId)) {
      upvoteButton.style.backgroundColor = "#888";
    }
  }

  // displays the number of upvotes a post has 
  const upvoteContent = createUpvoteContent(data);

  const subseddit = document.createElement("div");
  subseddit.classList.add("post-subseddit");
  subseddit.textContent = "s/" + data.meta.subseddit;

  const comments = document.createElement("div");
  comments.classList.add("post-comments")
  comments.textContent = data.comments.length + " Comments";

  parent.appendChild(post);
  post.appendChild(upvotes);
  upvotes.appendChild(upvoteButton);
  upvoteButton.appendChild(upvoteButtonImg);
  upvotes.appendChild(upvoteContent);
  post.appendChild(thumbnail);
  post.appendChild(content);
  content.appendChild(title);
  content.appendChild(postText);
  postText.appendChild(postTextNode);
  content.appendChild(subseddit);
  content.appendChild(author);
  author.appendChild(authorTextNode);
  content.appendChild(comments);
}

// removes all children under feed 
const removeAllPosts = () => {
  const feed = document.getElementById("feed");
  while (feed.firstChild) {
    feed.firstChild.remove();
  }
}

// lists all the comments on a post 
const populateComments = (data, parent, apiUrl) => {
  // window that contains the comments for the post 
  const commentContent = document.createElement("div");
  commentContent.id = "comment-content";
  commentContent.classList.add("comment-content");
  parent.appendChild(commentContent);

  // allows input for user comments 
  const commentText = document.createElement("textarea");
  commentText.classList.add("comment-textarea");
  commentText.placeholder = "Make a comment here...";
  commentContent.appendChild(commentText);

  const commentHeader = document.createElement("div");
  commentHeader.id = "comment-header";
  commentContent.appendChild(commentHeader);

  const commentsHeading = document.createElement("h4");
  if (data.comments.length === 0) {
    commentsHeading.textContent = 'Be the first to comment!';
    commentHeader.appendChild(commentsHeading);
  }

  const commentButton = document.createElement("button");
  commentButton.textContent = "comment";
  commentButton.className = "button button-primary";
  commentHeader.appendChild(commentButton);

  commentButton.addEventListener('click', () => {
    postComment(apiUrl, data.id, commentText);
  })

  const commentContainer = document.createElement("div");
  commentContainer.id = "comment-container";
  commentContent.appendChild(commentContainer);

  for (const element in data.comments) {
    const comments = document.createElement("div");
    comments.classList.add("user-comments");
    comments.textContent = data.comments[element].comment;

    const commentDate = new Date(data.comments[element].published * 1000);
    const commentDateText = `${commentDate.getDate()}/${commentDate.getMonth() + 1  }/${commentDate.getFullYear()}`;

    const byUser = document.createElement("p");
    const byUserTextNode = document.createTextNode(`by ${data.comments[element].author} on ${commentDateText}`);
    byUser.classList.add("post-author");
    byUser.appendChild(byUserTextNode);

    commentContainer.appendChild(comments);
    comments.appendChild(byUser);
  }
}

// lists users who upvoted a post 
const populateUpvotes = (data, parent, apiUrl) => {
  const upvoteHeader = document.createElement("h4");
  if (data.length === 0) {
    upvoteHeader.textContent = "Be the first to upvote the post!"
  } else {
    upvoteHeader.textContent = "Users who upvoted this post";
  }

  parent.appendChild(upvoteHeader);

  const upvoteList = document.createElement("ul");
  parent.appendChild(upvoteList);

  data.forEach((element) => {
    fetch(`${apiUrl}/user/?id=${element}`, {
        headers: {
          'Authorization': "Token " + window.token,
          'id': element
        }
      })
      .then((response) => {
        return response.json();
      })
      .then((user) => {
        const upvoteContentUser = document.createElement("li");
        upvoteContentUser.classList.add("upvoted-user");
        upvoteContentUser.textContent = `${user.username}`;
        upvoteList.appendChild(upvoteContentUser);
      })
  });
}

// sends a request to the API to upvote a post 
const upvotePost = (apiUrl, post_id, content, button) => {
  fetch(`${apiUrl}/post/vote?id=${post_id}`, {
      method: 'PUT',
      headers: {
        'Authorization': `Token ${window.token}`
      }
    })
    .then((response) => response.json())
    .then((message) => {
      // live updates the upvotes 
      return fetch(`${apiUrl}/post/?id=${post_id}`, {
        method: 'GET',
        headers: {
          'Authorization': `Token ${window.token}`
        }
      })
    })
    .then((response) => response.json())
    .then((post) => {
      content.textContent = post.meta.upvotes.length;
      button.style.backgroundColor = "#888";
      button.clicked = true;
      window.upvotes++;
    })
}

const loadUserFeed = (apiUrl) => {
  window.location.hash = "s/all";

  refreshFeed(apiUrl);
  populateFeed(apiUrl, "/user/feed");
  document.getElementById("feed-public").classList.remove("active");
  document.getElementById("feed-user").classList.add("active");
}

const loadPublicFeed = (apiUrl) => {
  window.location.hash = "";

  refreshFeed(apiUrl);
  populateFeed(apiUrl, "/post/public");
  removeDropDown();
  document.getElementById("feed-user").classList.remove("active");
  document.getElementById("feed-public").classList.add("active");
}

// sends a request to the API to make a post
const makePost = (apiUrl) => {
  let postFormSubseddit = document.getElementById("postForm-subseddit").value;
  // defaults the value of the subseddit to s/all if non existent
  if (postFormSubseddit === "") {
    postFormSubseddit = "all";
  }

  fetch(`${apiUrl}/post/`, {
      method: 'POST',
      headers: {
        'Authorization': `Token ${window.token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        title: document.getElementById("postForm-title").value,
        text: document.getElementsByClassName("form-textarea")[0].value,
        subseddit: postFormSubseddit,
        image: window.encodedImage
      })
    })
    .then((response) => response.json())
    .then((postId) => {
      console.log(postId);
      document.getElementById("post-window").style.display = "none";
      postForm.reset();
      // live updates the post 
      refreshFeed(apiUrl);
      document.getElementById("feed-public").click();
    })
}

// deletes user upvote
const deleteUpvote = (apiUrl, post_id, content, button) => {
  fetch(`${apiUrl}/post/vote?id=${post_id}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Token ${window.token}`
      }
    })
    .then((response) => response.json())
    .then((message) => {
      // live updates the upvotes 
      return fetch(`${apiUrl}/post/?id=${post_id}`, {
        method: 'GET',
        headers: {
          'Authorization': `Token ${window.token}`
        }
      })
    })
    .then((response) => response.json())
    .then((post) => {
      content.textContent = post.meta.upvotes.length;
      button.style.backgroundColor = "";
      button.clicked = false;
      window.upvotes--;
      console.log(window.upvotes);
    })
}

const createFeedContainer = () => {
  const feedContainer = document.createElement("ul");
  feedContainer.id = "feed";
  feedContainer.dataset.idFeed = "";

  return feedContainer;
}

const createUpvoteContent = (data) => {
  const upvoteContent = document.createElement("div");
  upvoteContent.classList.add("post-upvote-content");
  upvoteContent.dataset.idUpvotes = "";
  upvoteContent.textContent = data.meta.upvotes.length;

  return upvoteContent;
}

const getUserId = (apiUrl) => {
  fetch(`${apiUrl}/user/`, {
      headers: {
        'Authorization': `Token ${window.token}`
      }
    })
    .then((response) => response.json())
    .then((user) => {
      console.log(user);
      window.userId = user.id;
      window.username = user.username;
    });
}

// loads more posts when the user has reached the bottom of the page
const loadMore = (e, apiUrl) => {
  const element = e.target.scrollingElement;
  // only triggers once the user has reached the bottom of page
  if (element.scrollHeight - element.scrollTop === element.clientHeight) {
    fetch(`${apiUrl}/user/feed?p=${window.lastPost}&n=10`, {
        headers: {
          'Authorization': `Token ${window.token}`
        }
      })
      .then((response) => response.json())
      .then((data) => {
        for (const post in data.posts) {
          createPost(data.posts[post], apiUrl, feed);
          // stores the last post id to allow infinite scrolling 
          window.lastPost++;
        }
      })
  }
}

const generateOwnProfile = (apiUrl, id) => {
  fetch(`${apiUrl}/user/?id=${id}`, {
      headers: {
        'Authorization': `Token ${window.token}`
      }
    })
    .then((response) => response.json())
    .then((user) => {
      createOwnProfileContent(user, apiUrl);
    })
}

// initizlies the content of your profile
const createOwnProfileContent = (user, apiUrl) => {
  const profileUsername = user.username;
  const profileId = user.id;
  const profileFollowing = user.following;
  const profilePosts = user.posts;

  const profileContainer = document.createElement("div");
  profileContainer.classList.add("profile-container");
  profileContainer.id = "profile-container";
  document.getElementById("profile-window").appendChild(profileContainer);

  const profileHeading = document.createElement("h1");
  profileHeading.textContent = `${profileUsername}`;
  profileHeading.classList.add("profile-heading");
  profileContainer.appendChild(profileHeading);

  const profileExtra = document.createElement("h4");
  profileExtra.textContent = `id: ${profileId} - (upvotes given: ${window.upvotes})`
  profileContainer.appendChild(profileExtra);

  const profileInfoContainer = document.createElement("div");
  profileInfoContainer.classList.add("tab");
  profileContainer.appendChild(profileInfoContainer);

  const profilePostTab = document.createElement("button");
  profilePostTab.textContent = "View Posts";
  profileInfoContainer.appendChild(profilePostTab);

  // produces a feed replica but instead for the users post 
  profilePostTab.addEventListener('click', () => {
    profilePostTab.classList.add("active");
    profileFollowingTab.classList.remove("active");
    profileUpdateDetails.classList.remove("active");
    profileContent.textContent = "";

    postContent(profilePosts, apiUrl, profileContent);    
  })

  const profileFollowingTab = document.createElement("button");
  profileFollowingTab.textContent = "Following"
  profileInfoContainer.appendChild(profileFollowingTab);

  // displays the users you are following 
  profileFollowingTab.addEventListener('click', () => {
    profileFollowingTab.classList.add("active");
    profilePostTab.classList.remove("active");
    profileUpdateDetails.classList.remove("active");
    profileContent.textContent = "";
    
    followingContent(profileContent, profileFollowing);
  })

  const profileUpdateDetails = document.createElement("button");
  profileUpdateDetails.textContent = "Update details";
  profileUpdateDetails.id = "profile-update";
  profileInfoContainer.appendChild(profileUpdateDetails);

  profileUpdateDetails.addEventListener('click', () => {
    profileUpdateDetails.classList.add("active");
    profilePostTab.classList.remove("active");
    profileFollowingTab.classList.remove("active");
    profileContent.textContent = "";

    updateDetailContent(apiUrl, profileContent);
  })

  const profileContent = document.createElement("div");
  profileContent.classList.add("profile-content");
  profileContainer.appendChild(profileContent);

  profilePostTab.click();
}

// populates the post tab 
const postContent = (profilePosts, apiUrl, profileContent) => {
  if (profilePosts.length === 0) {
    const noPosts = document.createElement("h4");
    noPosts.textContent = "No posts made";
    profileContent.appendChild(noPosts);
  }

  profilePosts.forEach(element => {
    fetch(`${apiUrl}/post/?id=${element}`, {
        headers: {
          'Authorization': `Token ${window.token}`
        }
      })
      .then((response) => response.json())
      .then((data) => {
        createPostFake(data, apiUrl, profileContent);
      })
  });
}

// populates the content of the following tab
const followingContent = (profileContent, following) => {
  const tabText = document.createElement("h4");
  tabText.textContent = "You are currently following: ";
  profileContent.appendChild(tabText);

  const followingList = document.createElement("ul");
  profileContent.appendChild(followingList);

  if (following.length === 0) {
    tabText.textContent = "Following no users";
  }

  following.forEach(element => {
    const following = document.createElement("li");
    following.textContent = element;
    followingList.appendChild(following);
  });
}

// populates the content of the update detail tab
const updateDetailContent = (apiUrl, profileContent) => {
  const updateName = document.createElement("input");
  updateName.type = "text";
  updateName.placeholder = "name";

  const updateNameButton = document.createElement("button");
  updateNameButton.className = "button button-primary";
  updateNameButton.textContent = "update name";

  updateNameButton.addEventListener('click', () => {
    // makes sure name is not blank when updating
    if (!/^[^ ]+/.test(updateName.value)) {
      success.textContent = "name can't be empty";
      success.style.color = "red";
      return;
    }
    fetch(`${apiUrl}/user/`, {
        method: 'PUT',
        headers: {
          'Authorization': `Token ${window.token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          name: updateName.value
        })
      })
      .then((response) => response.json())
      .then((status) => {
        console.log(status);
        updateName.value = "";
        success.textContent = "details updated!";

        success.style.color = "rgb(68, 248, 92)";

      })
  })

  const updateEmail = document.createElement("input");
  updateEmail.type = "email";
  updateEmail.placeholder = "email";

  const updateEmailButton = document.createElement("button");
  updateEmailButton.className = "button button-primary";
  updateEmailButton.textContent = "update email";

  updateEmailButton.addEventListener('click', () => {
    // regex for proper email format
    if (!/^[^ ]+@[^ ]+\.[^ ]+/.test(updateEmail.value)) {
      success.textContent = "email can't be empty";
      success.style.color = "red";
      return;
    }
    fetch(`${apiUrl}/user/`, {
        method: 'PUT',
        headers: {
          'Authorization': `Token ${window.token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          email: updateEmail.value
        })
      })
      .then((response) => response.json())
      .then((status) => {
        console.log(status);
        updateEmail.value = "";
        success.textContent = "details updated!";
        success.style.color = "rgb(68, 248, 92)";
      })
  })

  const updatePassword = document.createElement("input");
  updatePassword.type = "password";
  updatePassword.placeholder = "password";

  const updatePasswordButton = document.createElement("button");
  updatePasswordButton.className = "button button-primary";
  updatePasswordButton.textContent = "update password";

  updatePasswordButton.addEventListener('click', () => {
    if (updatePassword.value.length === 0) {
      success.textContent = "password can't be empty";
      success.style.color = "red";
      return;
    }
    fetch(`${apiUrl}/user/`, {
        method: 'PUT',
        headers: {
          'Authorization': `Token ${window.token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          password: updatePassword.value
        })
      })
      .then((response) => response.json())
      .then((status) => {
        console.log(status);
        updatePassword.value = "";
        success.textContent = "details updated!";
        success.style.color = "rgb(68, 248, 92)";
      })
  })

  const success = document.createElement("div");


  profileContent.appendChild(updateName);
  profileContent.appendChild(updateNameButton);
  profileContent.appendChild(updateEmail);
  profileContent.appendChild(updateEmailButton);
  profileContent.appendChild(updatePassword);
  profileContent.appendChild(updatePasswordButton);
  profileContent.appendChild(success);
}

// generates profile for other users e.g. information such as which people they follow 
// are not shown 
const generateProfile = (apiUrl, username) => {
  fetch(`${apiUrl}/user/?username=${username}`, {
      headers: {
        'Authorization': `Token ${window.token}`
      }
    })
    .then((response) => response.json())
    .then((user) => {
      createProfileContent(user, apiUrl);
    })
}

// genereates the content of a general profile 

const createProfileContent = (user, apiUrl) => {
  const profileUsername = user.username;
  const profileName = user.name;
  const profileId = user.id;
  const profileEmail = user.email;
  const profileFollowing = user.following;
  const profileFollowed = user.followed_num;
  const profilePosts = user.posts;

  const profileContainer = document.createElement("div");
  profileContainer.classList.add("profile-container");
  profileContainer.id = "gen-profile-container";
  document.getElementById("profile-window").appendChild(profileContainer);

  const profileHeading = document.createElement("h1");
  profileHeading.textContent = `${profileUsername} (id: ${profileId})`;
  profileHeading.classList.add("profile-heading");
  profileContainer.appendChild(profileHeading);

  const followContainer = document.createElement("div");
  followContainer.id = "follow-container";
  profileContainer.appendChild(followContainer);

  const profileExtra = document.createElement("button");
  profileExtra.className = "button button-primary";
  profileExtra.id = "follow-button"

  if (window.follows.includes(profileUsername)) {
    profileExtra.textContent = "unfollow";
    profileExtra.classList.add("active")
  } else {
    profileExtra.textContent = "follow";
  }

  followContainer.appendChild(profileExtra);

  profileExtra.addEventListener('click', () => {
    if (profileExtra.classList.contains("active")) {
      unfollowUser(apiUrl, profileUsername);
    } else {
      followUser(apiUrl, profileUsername);
    }
  })

  const profileInfoContainer = document.createElement("div

  profileInfoContainer.classList.add("tab");
  profileContainer.appendChild(profileInfoContainer);

  const profilePostTab = document.createElement("button");

  profilePostTab.textContent = "View Posts";
  profileInfoContainer.appendChild(profilePostTab);

  profilePostTab.addEventListener('click', () => {
    profilePostTab.classList.add("active");
    profileFollowingTab.classList.remove("active");
    profileContent.textContent = "";

    postContent(profilePosts, apiUrl, profileContent);
  })

  const profileFollowingTab = document.createElement("button");
  profileFollowingTab.textContent = "Following"
  profileInfoContainer.appendChild(profileFollowingTab);

  profileFollowingTab.addEventListener('click', () => {
    profileFollowingTab.classList.add("active");
    profilePostTab.classList.remove("active");
    profileContent.textContent = "";

    const followingText = document.createElement("h4");
    followingText.textContent = `${profileUsername} is following ${profileFollowing.length} users`;
    profileContent.appendChild(followingText);
  })

  const profileContent = document.createElement("div");
  profileContent.classList.add("profile-content");
  profileContainer.appendChild(profileContent);

  profilePostTab.click();
}

// sends a request to the API to follow a user 
const followUser = (apiUrl, username) => {
  fetch(`${apiUrl}/user/follow?username=${username}`, {
      method: 'PUT',
      headers: {
        'Authorization': `Token ${window.token}`
      }
    })
    .then((response) => response.json())
    .then((result) => {
      const followButton = document.getElementById("follow-button");
      followButton.classList.add("active");
      window.follows.push(username);
      followButton.textContent = "unfollow";
    })
}

// sends a request to the API to unfollow a user 
const unfollowUser = (apiUrl, username) => {
  fetch(`${apiUrl}/user/unfollow?username=${username}`, {
      method: 'PUT',
      headers: {
        'Authorization': `Token ${window.token}`
      }
    })
    .then((response) => response.json())
    .then((result) => {
      const followButton = document.getElementById("follow-button");
      followButton.classList.remove("active");
      // removes the user from window.follows once you unfollow them
      window.follows = window.follows.filter((users) => users !== username);
      followButton.textContent = "follow";
    })
}

// sends a request to the API to post a comment with the comment 
// being derived from commentBox.value
const postComment = (apiUrl, postId, commentBox) => {
  fetch(`${apiUrl}/post/comment?id=${postId}`, {
      method: 'PUT',
      headers: {
        'Authorization': `Token ${window.token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        comment: commentBox.value
      })
    })
    .then((response) => response.json())
    .then((status) => {
      return fetch(`${apiUrl}/post/?id=${postId}`, {
        headers: {
          'Authorization': `Token ${window.token}`
        }
      })
    })
    .then((response) => response.json())
    .then((data) => {
      document.getElementById("comment-content").remove();
      if (document.getElementById("feed-public").classList.contains("active")) {
        document.getElementById("feed-public").click();
      } else {
        document.getElementById("feed-user").click();
      }
      // live updates 
      populateComments(data, document.getElementById("comment-window"), apiUrl);
    })
}

// appends the users you are following to the array window.follows
const getFollowers = (apiUrl) => {
  fetch(`${apiUrl}/user`, {
      headers: {
        'Authorization': `Token ${window.token}`
      }
    })
    .then((response) => response.json())
    .then((user) => {
      user.following.forEach(followers => {
        fetch(`${apiUrl}/user/?id=${followers}`, {
            headers: {
              'Authorization': `Token ${window.token}`
            }
          })
          .then((response) => response.json())
          .then((follower) => {
            window.follows.push(follower.username);
          })
      });
    })
}

// refreshes the feed to rpovide live updates
const refreshFeed = (apiUrl) => {
  removeAllPosts();
  document.getElementById("content").appendChild(createFeedContainer());
  createFeed(apiUrl);
}

export default initApp;
