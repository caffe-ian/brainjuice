
(function ($) {

  $window = $(window);

  // Play initial animations on page load.
    $window.on('load', function() {
      document.body.style.backgroundImage = `url(../assets/css/images/bg${Math.floor(Math.random() * 6)}.png)`;
    });

    $("#title").on('input', function() {
      document.querySelector(".poll-title").innerHTML = this.value;
    });

    $("#description").on('input', function() {
      let desc = this.value;
      let images = desc.match(/https:\/\/cdn\.discordapp\.com\/attachments\/\d+\/\d+\/[^\s]+\.(png|jpg|jpeg|gif)/ig);

      for (let image in images) {
        image = images[image];
        
        desc = desc.replace(image, `<img src="${image}" style="width:100%"/>`)
      }
      document.querySelector(".poll-description").innerHTML = desc;
    });

    $("#amount").on('input', function() {
      if (document.querySelector('input[type="radio"]:checked').value == "Fund request") {
        if (this.value != undefined && this.value != '') {
          document.querySelector(".poll-type > sep").innerHTML = "Fund request " + parseFloat(this.value) + " ETH";
        }
      }
    });

    $("input[type='radio']").click(() => {
      document.querySelector(".poll-type > sep").innerHTML = document.querySelector('input[type="radio"]:checked').value;
      if (document.getElementById("fundrequest").checked) {
        document.getElementById("amount-label").style.removeProperty("opacity");
        document.getElementById("amount").style.removeProperty("height");
        document.getElementById("amount").style.removeProperty("border");
        document.getElementById("amount").style.removeProperty("box-shadow");
        document.getElementById("amount").setAttribute("required", "");
      } else {
        document.getElementById("amount-label").style.opacity = 0;
        document.getElementById("amount").value = '';
        document.getElementById("amount").style.height = 0;
        document.getElementById("amount").style.border = "none";
        document.getElementById("amount").style.boxShadow = "none";
        document.getElementById("amount").removeAttribute("required");
      }
    });

})(jQuery);

async function gotoVoting() {
  window.provider = await web3Modal.connect();
  web3 = new Web3(provider);
  if (localStorage.getItem((await web3.eth.getAccounts())[0]) != null) {
    $.redirectPost("/voting", {'account': (await web3.eth.getAccounts())[0], 'access_token': localStorage.getItem((await web3.eth.getAccounts())[0])});
    return;
  }
  document.getElementById("transition").classList.add("white");

  window.setTimeout(function () {
    window.location = "/verify?loc=voting";
  }, 1000);
}

function createPoll() {
  let discord_id = document.getElementById("discord_id").value;
  let cost = document.getElementById("amount").value || 0;
  try {
    cost = parseFloat(cost);
    if (cost == NaN) {
      alert("Invalid cost");
      return;
    } 
  } catch {
    alert("Invalid cost");
    return;
  }
  if (cost !== 0 && cost < 0.01) {
    alert("Cost cannot be lesser than 0.01 ETH");
    return;
  } else if (cost > 1) {
    alert("Cost cannot be more than 1 ETH");
    return;
  } else if (Math.floor(cost) !== cost && cost.toString().split(".")[1].length > 3) {
    alert("Cost can only have 3 decimals. Example: 0.015");
    return;
  }
  let type = document.querySelector('input[name="type"]:checked').value;
  if (type == "Fund request") {
    type = type + ` ${cost} ETH`;
  }
  let title = document.getElementById("title").value;
  if (title.length < 4 || title.length > 50) {
    alert("Title must be between 4 to 50 characters");
    return
  }
  let description = document.getElementById("description").value.replace(/(\r\n|\r|\n){2,}/g, '\n');
  if (description.length < 10 || description.length > 400) {
    alert("Description must be between 10 to 400 characters");
    return;
  }
  $.post("/poll", {"address": address, "access_token": localStorage.getItem(address), "discord_id": discord_id, "type": type, "title": title, "description": description}, (result) => {
    if (result !== true) {
      alert(result, "Creating poll failed..");
      return;
    } else {
      gotoVoting();
    }
  });
}

function countCharacter(element) {
  document.getElementById(`${element.id}-counter`).innerHTML = element.value.length + "/" + element.maxLength;
}
