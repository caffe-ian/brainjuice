
(function ($) {

  $window = $(window);

  // Play initial animations on page load.
    $window.on('load', async function() {
      $.post("/userdata", {"address": address, "access_token": localStorage.getItem(address)}, (result) => {
        window.userdata = result;
        updateData(userdata);
      });
    });

  $('.showcase-la').on({
      'mousedown touchstart': function () {
          $(".showcase").animate({scrollLeft: 0}, 1000);
      },
      'mouseup touchend': function () {
          $(".showcase").stop(true);
      }
  });

  $('.showcase-ra').on({
      'mousedown touchstart': function () {
          $(".showcase").animate({
              scrollLeft: $(".showcase")[0].scrollWidth - $(".showcase")[0].clientWidth
          }, 1000);
      },
      'mouseup touchend': function () {
          $(".showcase").stop(true);
      }
});

})(jQuery);

function copy(copyText) {
  copyText = copyText.innerHTML;
  navigator.clipboard.writeText(copyText);
  alert("Address copied to clipboard", "Success")
}

function getTime(createdAt) {
  let time = Math.round((createdAt + 259200) - Math.floor(Date.now() / 1000));
  if (time > 0) {
    let d = Math.floor(time / (3600*24));
    let h = Math.floor(time % (3600*24) / 3600);
    let m = Math.floor(time % 3600 / 60);
    let s = Math.floor(time % 60);

    let dDisplay = d > 0 ? d + "d " : "";
    let hDisplay = h > 0 ? h + "h " : "";
    let mDisplay = m > 0 ? m + "m " : "";
    let sDisplay = s > 0 ? s + "s" : "";
    return dDisplay + hDisplay + mDisplay + sDisplay;
  } else {
    return "Expired";
  }
}

function pollTime() {
  let polltime = document.getElementsByClassName("poll-time");
  polltime = Array.from(polltime);
  for (let poll in polltime) {
    poll = polltime[poll];
    if (poll.innerHTML != "Expired") {
      poll.innerHTML = getTime(parseInt(poll.getAttribute("value")));
    }
  }
}

async function updateData(data) {
  document.getElementById("ownednfts").innerHTML = "BrainJ NFTs owned: " + data.nftCount;
  document.getElementById("balance").innerHTML = data.bank + " ETH";
  for (let nft in data.nftsOwned) {
    nft = data.nftsOwned[nft].split("metadata/")[1].split(".")[0];
    let nftdiv = document.createElement("div");
    nftdiv.classList.add("showcase-image");
    nftdiv.innerHTML = `<img src="https://brainjuicenft.up.railway.app/api/image/${nft}.png" style="border-radius: 10px;"/>
                        <h2 class="showcase-name">Brain Juice #${('000' + nft).slice(-4).replace("dden", "????")}</h2>`;
    document.getElementsByClassName("showcase")[0].appendChild(nftdiv);
  }
  let container = document.getElementsByClassName("poll-container")[0];
  if (!Array.isArray(polls) && polls != 0) {
    polls = [polls];
  }
  if (!Array.isArray(owned) && owned != 0) {
    owned = [owned];
  }
  if (polls != '') {
    let i = 0;
    for (let poll in polls) {
      poll = polls[poll];
      i += 1;
      let polldiv = document.createElement("div");
      polldiv.classList.add("poll");
      if (poll.pinned == true) {
        polldiv.classList.add("pinned");
        poll.div.innerHTML = `<p class="pinned">Pinned</p>`;
      } 
      if (i == 2) {
        polldiv.classList.add("second-poll");
      } else if (i == 3) {
        polldiv.classList.add("third-poll");
      }
      let id = poll.id
      polldiv.innerHTML += `<h2 id="poll-${id}" class="poll-id"><a href="#poll-${id}">#${id}</a> • ${poll.verified?'Verified':'Unverified'}</h2>
                    <a class="report-button" onclick="report(this)">Report</a>
                    <div class="poll-header">
                      <p class="poll-author">Discord ID • <sep>${poll.discord_id}</sep></p>
                      <p class="poll-type">Type • <sep>${poll.type}${poll.type == "Fund request"?" "+poll.cost+" ETH":""}</sep></p>
                    </div>
                    <h2 class="poll-title">${poll.title}</h2>
                    <hr class="poll-hr">
                    <p class="poll-description">${poll.description}</p>
                    <p class="poll-time" value="${poll.createdAt}">${getTime(poll.createdAt)}</p>
                    <div class="poll-votes">
                      <a onclick="dope(this)" class="poll-dope">DOPE<br><sep>${poll.dope}</sep></a>
                      <a onclick="nope(this)" class="poll-nope">NOPE<br><sep>${poll.nope}</sep></a>
                    </div>`;
      if (owned.includes(id)) {
        polldiv.children[1].innerHTML = "Discard";
        polldiv.children[1].setAttribute("onclick", "discard(this)");
        if (poll.type == "Fund request" && poll.claimed == false && Math.round((poll.createdAt + 259200) - Math.floor(Date.now() / 1000)) <= 0) {
          polldiv.children[6].classList.remove('poll-time');
          polldiv.children[6].classList.add('poll-claim');
          polldiv.children[6].innerHTML = "<a onclick='claimFund(this)'>Claim Funds</a>";
        } else if (poll.type == "Fund request" && poll.claimed == true) {
          polldiv.children[6].classList.remove('poll-time');
          polldiv.children[6].classList.add('poll-claimed');
          polldiv.children[6].innerHTML = "Funds claimed";
        }
      }
      if (votes !== 0 && votes.upvoted.includes(id)) {
        polldiv.children[7].children[0].classList.toggle("selected");
      } else if (votes !== 0 && votes.downvoted.includes(id)) {
        polldiv.children[7].children[1].classList.toggle("selected");
      }
      let desc = polldiv.children[5].innerHTML;
      let images = desc.match(/https:\/\/cdn\.discordapp\.com\/attachments\/\d+\/\d+\/[^\s]+\.(png|jpg|jpeg|gif)/ig);

      for (let image in images) {
        image = images[image];
        
        desc = desc.replace(image, `<a style="border-bottom:none"><img href="${image}" src="${image}" style="width:100%"/></a>`)
      }
      polldiv.children[5].innerHTML = desc;
      container.appendChild(polldiv);
    }
  } else {
    let polldiv = document.createElement("div");
    polldiv.classList.add("poll");
    polldiv.innerHTML = `<h2 class="poll-id"><a>#0</a></h2>
                  <a class="report-button">Report</a>
                  <div class="poll-header">
                    <p class="poll-author">Discord ID • <sep></sep></p>
                    <p class="poll-type">Type • <sep></sep></p>
                  </div>
                  <h2 class="poll-title">No polls available</h2>
                  <hr class="poll-hr">
                  <p class="poll-description">No polls available</p>
                  <p class="poll-time" value="0"></p>
                  <div class="poll-votes">
                    <a class="poll-dope">DOPE<br><sep>0</sep></a>
                    <a class="poll-nope">NOPE<br><sep>0</sep></a>
                  </div>`;
    container.appendChild(polldiv);
  }
  setInterval(pollTime, 1000);
}

function dope(element) {
  let id = parseInt(element.parentElement.parentElement.children[0].children[0].innerHTML.split("#")[1]);
  let discord_id = element.parentElement.parentElement.children[2].children[0].innerHTML.split("<sep>")[1].split("</sep>")[0];
  let type = element.parentElement.parentElement.children[2].children[1].innerHTML.split("<sep>")[1].split("</sep>")[0];
  let title = element.parentElement.parentElement.children[3].innerHTML;
  let description = element.parentElement.parentElement.children[5].innerHTML;
  let dope = parseInt(element.parentElement.parentElement.children[7].children[0].innerHTML.split("<sep>")[1].split("</sep>")[0]);
  let nope = parseInt(element.parentElement.parentElement.children[7].children[1].innerHTML.split("<sep>")[1].split("</sep>")[0]);
  element.classList.toggle("selected");
  document.querySelectorAll(".poll-dope, .poll-nope").forEach((element) => {
    element.style.pointerEvents = "none";
  });
  setTimeout(() => {
    document.querySelectorAll(".poll-dope, .poll-nope").forEach((element) => {
      element.style.pointerEvents = "auto";
    });
  }, 1000);
  $.post("/dope", {"address": address, "access_token": localStorage.getItem(address), "id": id, "discord_id": discord_id, "type": type, "title": title, "description": description, "dope": dope, "nope": nope}, (result) => {
    if (isNaN(parseInt(result))) {
      element.classList.toggle("selected");
      alert(result, "Voting failed..");
      return;
    } else {
      element.parentElement.parentElement.children[7].children[1].classList.remove("selected");
      if (result !== 0) {
        element.children[1].innerHTML = parseInt(element.children[1].innerHTML) + result;
      } else {
        element.children[1].innerHTML = parseInt(element.children[1].innerHTML) + 1;
        element.parentElement.children[1].children[1].innerHTML = parseInt(element.parentElement.children[1].children[1].innerHTML) - 1;
      }
    }
  });
}

function nope(element) {
  let id = parseInt(element.parentElement.parentElement.children[0].children[0].innerHTML.split("#")[1]);
  let discord_id = element.parentElement.parentElement.children[2].children[0].innerHTML.split("<sep>")[1].split("</sep>")[0];
  let type = element.parentElement.parentElement.children[2].children[1].innerHTML.split("<sep>")[1].split("</sep>")[0];
  let title = element.parentElement.parentElement.children[3].innerHTML;
  let description = element.parentElement.parentElement.children[5].innerHTML;
  let dope = parseInt(element.parentElement.parentElement.children[7].children[0].innerHTML.split("<sep>")[1].split("</sep>")[0]);
  let nope = parseInt(element.parentElement.parentElement.children[7].children[1].innerHTML.split("<sep>")[1].split("</sep>")[0]);
  element.classList.toggle("selected");
  document.querySelectorAll(".poll-dope, .poll-nope").forEach((element) => {
    element.style.pointerEvents = "none";
  });
  setTimeout(() => {
    document.querySelectorAll(".poll-dope, .poll-nope").forEach((element) => {
      element.style.pointerEvents = "auto";
    });
  }, 1000);
  $.post("/nope", {"address": address, "access_token": localStorage.getItem(address), "id": id, "discord_id": discord_id, "type": type, "title": title, "description": description, "dope": dope, "nope": nope}, (result) => {
    if (isNaN(parseInt(result))) {
      element.classList.toggle("selected");
      alert(result, "Voting failed..");
      return;
    } else {
      element.parentElement.parentElement.children[7].children[0].classList.remove("selected");
      if (result !== 0) {
        element.children[1].innerHTML = parseInt(element.children[1].innerHTML) + result;
      } else {
        element.children[1].innerHTML = parseInt(element.children[1].innerHTML) + 1;
        element.parentElement.children[0].children[1].innerHTML = parseInt(element.parentElement.children[0].children[1].innerHTML) - 1;
      }
    }
  });
}

async function gotoVoting() {
  document.getElementById("transition").classList.add("white");
  if (localStorage.getItem(address) != null) {
    window.setTimeout(function () {
      $.redirectPost("/voting", {'account': address, 'access_token': localStorage.getItem(address)});
    }, 1000);
    return;
  }

  window.setTimeout(function () {
    window.location = "/verify?loc=voting";
  }, 1000);
}

function claimFund(element) {
  $.post("/claim-fund", {"address": address, "access_token": localStorage.getItem(address), "id": parseInt(element.parentElement.parentElement.children[0].children[0].innerHTML.split("#")[1])}, (result) => {
    if (result !== true) {
      alert(result);
      return;
    } else {
      alert("Funds has been successfully added to your bank", "Funds claimed!");
      element.parentElement.children[6].classList.remove('poll-claim');
      element.parentElement.children[6].classList.add('poll-claimed');
      element.parentElement.children[6].innerHTML = "Funds claimed";
    }
  });
}

function withdraw() {
  if (parseFloat(document.getElementById("balance").innerHTML.split(" ETH")[0]) < 0.01) {
    alert("You need at least 0.01 ETH to withdraw!");
    return;
  }
  alert("Please do not click anything until the transaction completes", "Please wait");
  $.post("/withdraw", {"address": address, "access_token": localStorage.getItem(address)}, (result) => {
    if (result !== true) {
      alert(result);
      return;
    } else {
      alert("Funds has been successfully withdrawed to your wallet!", "Funds withdrawed!");
      document.getElementById("balance").innerHTML = "0 ETH";
    }
  });
}
