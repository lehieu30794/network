document.addEventListener("DOMContentLoaded", function () {
  //   document.querySelector("#post_form").addEventListener("submit", () => submit_post);

  // New Post
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

  // All posts
  fetch("/post", {
    method: "GET",
  })
    .then((response) => response.json())
    .then((data) => {
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

  // Create each child element within post_content
  const post_author = document.createElement("p");
  post_author.innerHTML = `User: <strong style="color:green"> ${post.author} </strong>`;
  post_element.appendChild(post_author);

  const username_logged_in = document.querySelector("#username_logged_in");
  if (post.author == username_logged_in.innerHTML) {
    const post_edit_button = document.createElement("a");
    post_edit_button.innerHTML = "Edit";
    post_edit_button.href = "https://www.google.com/";
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
        post_element.appendChild(post_heart_empty);
        post_heart_empty.addEventListener("click", () => functionLikePost(post.id));
      } else {
        const post_heart = document.createElement("img");
        post_heart.src = "static/network/heart.png";
        post_heart.style.width = "15px";
        post_element.appendChild(post_heart);
      }
    })
    // Put the number of Post within this block, so it does not load before
    // all the hearts
    .then(() => {
      const post_like = document.createElement("span");
      post_like.innerHTML = "   #N";
      post_element.appendChild(post_like);

      document.querySelector("#all_posts").append(post_element);
    });

  //   const post_heart_empty = document.createElement("img");
  //   post_heart_empty.src = "static/network/heart_empty.png";
  //   post_heart_empty.style.width = "15px";
  //   post_element.appendChild(post_heart_empty);
  //   post_heart_empty.addEventListener("click", () => functionLikePost(post.id));

  //   const post_heart = document.createElement("img");
  //   post_heart.src = "static/network/heart.png";
  //   post_heart.style.width = "15px";
  //   post_element.appendChild(post_heart);

  //   const post_like = document.createElement("span");
  //   post_like.innerHTML = "   #N";
  //   post_element.appendChild(post_like);

  //   document.querySelector("#all_posts").append(post_element);
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
