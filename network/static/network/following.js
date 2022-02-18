document.addEventListener("DOMContentLoaded", function () {
  //   document.querySelector("#post_form").addEventListener("submit", () => submit_post);

  // Post new entry
  document.querySelector("#post_form").onsubmit = () => {
    console.log("Submit button clicked");
    alert("Submit button clicked");
    fetch("/post", {
      method: "POST",
      body: JSON.stringify({
        content: document.querySelector("#new_post").value,
      }),
    })
      .then((response) => response.json())
      .then((result) => {
        // Print result
        console.log(result);
      });
    // Remove value in textarea after submitted
    document.querySelector("#new_post").value = "";
    // Prevent the form from submitting
    return false;
  };

  //   JS solution to switch the api route did not work as it did not refresh
  //   Even if it does, it will always use the api route declare at the beginning
  //   let all_posts_api_route = "/all_posts";
  //   // If Follow button is click, change the API route to /following_posts
  //   const following_link = document.querySelector("#following_link");
  //   following_link.addEventListener("click", () => {
  //     all_posts_api_route = "/following_posts";
  //     alert(all_posts_api_route);
  //   });

  // Get all posts
  fetch(`/following_posts`, {
    method: "GET",
  })
    .then((response) => response.json())
    .then((data) => {
      // Hide the Edit section while showing all the posts
      document.querySelector("#edit_post").style.display = "none";
      document.querySelector("#profile").style.display = "none";
      console.log("Get Post data");
      console.log(data);
      data.forEach((item) => show_post(item));
    });
});

function show_post(post) {
  console.log("post content:");
  console.log(post);

  const post_element = document.createElement("div");
  post_element.className = "post";
  document.querySelector("#all_posts").append(post_element);

  // Create each child element within post_content
  const post_author = document.createElement("button");
  post_author.innerHTML = `<strong style="color:green"> ${post.author} </strong>`;
  post_author.className = "btn btn-link p-0 mb-2";
  post_author.style.display = "block";
  // View profile page
  post_author.addEventListener("click", () => functionProfilePage(post.author));
  post_element.appendChild(post_author);

  const username_logged_in = document.querySelector("#username_logged_in");
  if (post.author == username_logged_in.innerHTML) {
    const post_edit_button = document.createElement("button");
    post_edit_button.innerHTML = "Edit";
    post_edit_button.className = "btn btn-link p-0";
    // Open Edit form when clicking
    post_edit_button.addEventListener("click", () => functionEditPost(post.id));
    post_element.appendChild(post_edit_button);
  }

  const post_content = document.createElement("div");
  post_content.innerHTML = post.content;
  post_element.appendChild(post_content);

  const post_timestamp = document.createElement("div");
  post_timestamp.innerHTML = post.timestamp;
  post_element.appendChild(post_timestamp);

  // Determine if the user already liked the post. If yes, then show red heart; no => plain heart
  const post_id = post.id;
  fetch("/check_like", {
    method: "POST",
    body: JSON.stringify({
      post_id: post_id,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log(`Post is liked: ${data}`);

      if (data == false) {
        const post_heart_empty = document.createElement("img");
        post_heart_empty.src = "static/network/heart_empty.png";
        post_heart_empty.style.width = "15px";
        post_heart_empty.className = "empty_heart";
        post_element.appendChild(post_heart_empty);
        post_heart_empty.addEventListener("click", () => functionLikePost(post.id));
      } else {
        const post_heart = document.createElement("img");
        post_heart.src = "static/network/heart.png";
        post_heart.style.width = "15px";
        post_heart.className = "filled_heart";
        post_element.appendChild(post_heart);
        post_heart.addEventListener("click", () => functionUnlikePost(post.id));
      }
    })
    // Put the number of Post within this block, so it does not load before
    // all the hearts
    .then(() => {
      const post_like = document.createElement("span");
      const post_id = post.id;
      fetch("/like_num", {
        method: "POST",
        body: JSON.stringify({
          post_id: post_id,
        }),
      })
        .then((response) => response.json())
        .then((data) => {
          console.log(`"Number of likes: " ${data}`);
          //   post_like.innerHTML = "   #N";
          post_like.innerHTML = ` ${data}`;
          post_element.appendChild(post_like);
        });
    });
}

function functionLikePost(post_id) {
  fetch("/like", {
    method: "POST",
    body: JSON.stringify({
      post_id: post_id,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
    });
}

function functionUnlikePost(post_id) {
  fetch("/unlike", {
    method: "POST",
    body: JSON.stringify({
      post_id: post_id,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
    });
}

function functionEditPost(post_id) {
  fetch(`/post/${post_id}`)
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      document.querySelector("#all_post_title").style.display = "none";
      document.querySelector("#all_posts").style.display = "none";
      document.querySelector("#profile").style.display = "none";
      document.querySelector("#edit_post").style.display = "block";
      document.querySelector("#edit_post_text").innerHTML = `${data.content}`;

      // Edit Post
      document.querySelector("#edit_form").onsubmit = () => {
        console.log("Save button clicked");
        alert("Save button clicked");
        fetch(`/post/${post_id}`, {
          method: "POST",
          body: JSON.stringify({
            content: document.querySelector("#edit_post_text").value,
          }),
        })
          .then((response) => response.json())
          .then((result) => {
            // Print result
            console.log(result);
          });
        // Remove value in textarea after submitted
        document.querySelector("#new_post").value = "";

        // Reload the all posts after editted- like redirect
        document.querySelector("#all_post_title").style.display = "block";
        document.querySelector("#all_posts").style.display = "block";
        document.querySelector("#edit_post").style.display = "none";
        document.querySelector("#profile").style.display = "none";

        location.reload();

        // Prevent the form from submitting
        return false;
      };
    });
}

function functionProfilePage(username) {
  fetch(`profile/${username}`)
    .then((response) => response.json())
    .then((data) => {
      console.log("data");
      console.log(data);

      // Separate profile data at the end of the array
      const profile_data = data.pop();
      console.log("profile_data");
      console.log(profile_data);

      // Show profile data with relevant information
      document.querySelector("#all_post_title").style.display = "none";
      document.querySelector("#all_post_heading").style.display = "none";
      document.querySelector("#all_posts").style.display = "none";
      document.querySelector("#edit_post").style.display = "none";
      document.querySelector("#profile").style.display = "block";

      // Since there's only 1 item in the array, using [0] to get all the profile data
      document.querySelector("#username").innerHTML = `@${profile_data[0].post_user}`;
      document.querySelector("#followers").innerHTML = profile_data[0].follower_num;
      document.querySelector("#following").innerHTML = profile_data[0].following_num;
      document.querySelector("#post_num").innerHTML = profile_data[0].post_num;

      // Only show Follow button if accessing other users' page
      let username_logged_in = document.querySelector("#username_logged_in");
      username_logged_in = username_logged_in.innerHTML;
      if (profile_data[0].post_user.toLowerCase() == username_logged_in.toLowerCase()) {
        document.querySelector("#follow_button").style.display = "none";
      } else if (profile_data[0].already_followed === true) {
        const unfollow_button = document.querySelector("#follow_button");
        unfollow_button.innerHTML = "Unfollow";
        const post_user_name = profile_data[0].post_user;
        unfollow_button.addEventListener("click", () => functionUnfollow(post_user_name));
      } else {
        const follow_button = document.querySelector("#follow_button");
        follow_button.innerHTML = "Follow";
        const post_user_name = profile_data[0].post_user;
        follow_button.addEventListener("click", () => functionFollow(post_user_name));
      }

      console.log("data.posts");
      console.log(data.posts);

      data.forEach((item) => show_post_specific_user(item));
    });
}

function show_post_specific_user(post) {
  console.log("post content:");
  console.log(post);

  const post_element = document.createElement("div");
  post_element.className = "post";
  document.querySelector("#profile").append(post_element);

  // Create each child element within post_content
  const post_author = document.createElement("button");
  post_author.innerHTML = `<strong style="color:green"> ${post.author} </strong>`;
  post_author.className = "btn btn-link p-0 mb-2";
  post_author.style.display = "block";
  // View profile page
  post_author.addEventListener("click", () => functionProfilePage(post.author));
  post_element.appendChild(post_author);

  const username_logged_in = document.querySelector("#username_logged_in");
  if (post.author == username_logged_in.innerHTML) {
    const post_edit_button = document.createElement("button");
    post_edit_button.innerHTML = "Edit";
    post_edit_button.className = "btn btn-link p-0";
    // Open Edit form when clicking
    post_edit_button.addEventListener("click", () => functionEditPost(post.id));
    post_element.appendChild(post_edit_button);
  }

  const post_content = document.createElement("div");
  post_content.innerHTML = post.content;
  post_element.appendChild(post_content);

  const post_timestamp = document.createElement("div");
  post_timestamp.innerHTML = post.timestamp;
  post_element.appendChild(post_timestamp);
}

function functionFollow(post_user_name) {
  fetch(`/follow/${post_user_name}`, {
    method: "POST",
  })
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
    });
}
function functionUnfollow(post_user_name) {
  fetch(`/follow/${post_user_name}`, {
    method: "DELETE",
    body: JSON.stringify({
      post_user_name: post_user_name,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
    });
}

// function functionUnlikePost(post_id) {
//     fetch("/unlike", {
//       method: "POST",
//       body: JSON.stringify({
//         post_id: post_id,
//       }),
//     })
//       .then((response) => response.json())
//       .then((data) => {
//         console.log(data);
//       });
//   }

// const post_id = post.id;
// fetch("/check_like", {
//   method: "POST",
//   body: JSON.stringify({
//     post_id: post_id,
//   }),
// })
