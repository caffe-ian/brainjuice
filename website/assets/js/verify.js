(function ($) {

  $.extend(
  {
      redirectPost: function (location, args) {
          var form = $('<form>', { action: location, method: 'post' });
          $.each(args,
              function (key, value) {
                  $(form).append(
                      $('<input>', { type: 'hidden', name: key, value: value })
                  );
              });
          $(form).appendTo('body').submit();
      }
  });
})( jQuery );

async function verifyStart() {
  if (web3Modal.cachedProvider == '') {
    alert("No wallet connected.\nReturning to homepage in 5 seconds");
    window.setTimeout(function() {
      document.getElementById("transition").classList.add("white");

      window.setTimeout(function () {
        window.location = "/";
      }, 1000);
    }, 5000);
    return;
  }
  var url = new URL(window.location.href);
  var a = url.searchParams.get("a");
  if (a != undefined) {
    await removeKey();
  } else {
    await verifying();
  }
}

async function removeKey() {
  window.provider = await web3Modal.connect();
  web3 = new Web3(provider);
  var account = (await web3.eth.getAccounts())[0];
  localStorage.removeItem(account);
  window.location = "/verify?loc="+getParameterByName('loc');
}

function getParameterByName(name, url = window.location.href) {
    name = name.replace(/[\[\]]/g, '\\$&');
    var regex = new RegExp('[?&]' + name + '(=([^&#]*)|&|#|$)'),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, ' '));
}

async function verifying() {
  window.provider = await web3Modal.connect();
  web3 = new Web3(provider);
  let account = (await web3.eth.getAccounts())[0];
  let loc = "/" + getParameterByName('loc');
  if (loc == "/null") {
    loc = "/dashboard";
  }
  if (localStorage.getItem(account) == null) {
    let response = await fetch(`/request-nonce?account=${account}`);
    let data = await response.json();
    let signature;
    try {
      signature = await web3.eth.personal.sign(`Verify: nonce ${data["nonce"]}`, account);
    } catch {
      alert("Verification failed\nDid you cancelled?\nReturning to homepage in 5 seconds");
      window.setTimeout(function() {
        document.getElementById("transition").classList.add("white");

        window.setTimeout(function () {
          window.location = "/";
        }, 1000);
      }, 5000);
      return;
    }
    let errors = [account, data["nonce"], data["access_token"], signature];
    if (errors.includes("") || errors.includes(undefined) || errors.includes(null)) {
      alert("Verification failed\nIf you think this is a mistake, contact us in our Discord server");
      window.setTimeout(function() {
        document.getElementById("transition").classList.add("white");

        window.setTimeout(function () {
          window.location = "/";
        }, 1000);
      }, 5000);
      return;
    }
    localStorage.setItem(account, data["access_token"]);
    (function( $ ){
      if (getParameterByName('discord_id') != null) {
        $.redirectPost(loc, {'nonce': data["nonce"], 'signature': signature, 'access_token': data["access_token"], 'discord_id': getParameterByName('discord_id')});
        return;
      }
      $.redirectPost(loc, {'nonce': data["nonce"], 'signature': signature, 'access_token': data["access_token"]});
    })( jQuery );
  } else {
    if (getParameterByName('discord_id') != null) {
      $.redirectPost(loc, {'account': account, 'access_token': localStorage.getItem(account), 'discord_id': getParameterByName('discord_id')});
      return;
    }
    $.redirectPost(loc, {'account': account, 'access_token': localStorage.getItem(account)});
  }
}