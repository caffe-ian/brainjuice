
(function ($) {

  var  $window = $(window),
  $body = $('body'),
  $sidebar = $('#sidebar');

  // Breakpoints.
    breakpoints({
      xlarge:   [ '1281px',  '1680px' ],
      large:    [ '981px',   '1280px' ],
      medium:   [ '737px',   '980px'  ],
      small:    [ '481px',   '736px'  ],
      xsmall:   [ null,      '480px'  ]
    });

  // Hack: Enable IE flexbox workarounds.
    if (browser.name == 'ie')
      $body.addClass('is-ie');

  // Play initial animations on page load.
    $window.on('load', async function() {

      const Web3Modal = window.Web3Modal.default;
      const WalletConnectProvider = window.WalletConnectProvider.default;

      const providerOptions = {
        walletconnect: {
          display: {
            name: "WalletConnect",
            description: "Scan QR code with your mobile phone"
          },
          package: WalletConnectProvider,
          options: {
            infuraId: "0194fd40b77a4f03a28c0adcdc9a4d8b"
          }
        }
      };

      window.web3Modal = new Web3Modal({
        theme: {
          background: "rgba(65, 0, 71, 0.6)",
          hover: "rgba(52, 0, 57, 0.6)"
        },
        network: "mainnet",
        cacheProvider: true,
        providerOptions
      });

      window.setTimeout(function() {
        $('#transition').removeClass('white');
      }, 1000);
      let path = window.location.href.split("/");
        if (path[path.length-1].includes("#")) {
        window.setTimeout(function() {
          scroll(path[path.length-1].split("#")[1]);
        }, 1000);
      }
      window.setTimeout(function() {
        $body.removeClass('is-preload');
      }, 999);
      if (window.location.href.split("/")[window.location.href.split("/").length-1].startsWith("verify")) {
        await verifyStart();
      }
      await checkWallet();
      await verify();
    });

    $window.on('scroll', function() {
      if (!$window.scrollTop() == 0) {
        $(".top").addClass("show");
      } else {
        $(".top").removeClass("show");
      }
    });

  // Forms.

    // Hack: Activate non-input submits.
      $('form').on('click', '.submit', function(event) {

        // Stop propagation, default.
          event.stopPropagation();
          event.preventDefault();

        // Submit form.
          $(this).parents('form').submit();

      });

    $(document).on("click", "a", function (request) {

      let link = request.target.getAttribute("href");

      if (request.target.classList.contains("icon-2")) {
        link = "..";
      }

      if (link == null || link == "" || link == undefined) {
        request.preventDefault();
        return;
      } else if (link.startsWith("#")) {
        return;
      } else if (link.startsWith("wc:")) {
        request.preventDefault();
        window.location = link;
        return;
      }

      request.preventDefault();

      if (link.startsWith("$")) {
        document.getElementById("transition").classList.add("white");

        window.setTimeout(function () {
          history.back();
        }, 1000);
      } else {
        document.getElementById("transition").classList.add("white");

        window.setTimeout(function () {
          window.location.href = link;
        }, 1000);
        // window.open(link, '_blank').focus();
      }

      return;
    });

    $(".error").click(() => {
      closealert();
    }).children().click(() => {
      return false;
    });

    $(".rep").click(() => {
      closereport();
      closediscard();
    }).children().click(() => {
      return false;
    });

  // Sidebar

  if ($sidebar.length > 0) {

      var $sidebar_a = $sidebar.find('a');

      $sidebar_a
        .on('click', function() {

          var $this = $(this);

          // External link? Bail.
            if (!$this.attr('href').startsWith("#")) {
              return;
            }

          // Deactivate all links.
            $sidebar_a.removeClass('active');

          // Activate link *and* lock it (so Scrollex doesn't try to activate other links as we're scrolling to this one's section).
            $this
              .addClass('active')
              .addClass('active-locked');

        })
        .each(function() {

            var  $this = $(this),
            id = $this.attr('href'),
            $section = $(id);

          // No section for this link? Bail.
            if ($section.length < 1)
              return;

          // Scrollex.
            $section.scrollex({
              mode: 'middle',
              top: '-20vh',
              bottom: '-20vh',
              initialize: function() {

                // Deactivate section.
                  $section.addClass('inactive');

              },
              enter: function() {

                // Activate section.
                  $section.removeClass('inactive');

                // No locked links? Deactivate all links and activate this section's one.
                  if ($sidebar_a.filter('.active-locked').length == 0) {

                    $sidebar_a.removeClass('active');
                    $this.addClass('active');

                  }

                // Otherwise, if this section's link is the one that's locked, unlock it.
                  else if ($this.hasClass('active-locked'))
                    $this.removeClass('active-locked');

              }
            });

        });

    }

  // Scrolly.
    $('.scrolly').scrolly({
      speed: 2000,
      offset: function() {

        // If <=large, >small, and sidebar is present, use its height as the offset.
          if (breakpoints.active('<=large')
          &&  !breakpoints.active('<=small')
          &&  $sidebar.length > 0)
            return $sidebar.height();

        return 0;

      }
    });

  // Spotlights.
    $('.spotlights > section')
      .scrollex({
        mode: 'middle',
        top: '-10vh',
        bottom: '-10vh',
        initialize: function() {

          // Deactivate section.
            $(this).addClass('inactive');

        },
        enter: function() {

          // Activate section.
            $(this).removeClass('inactive');

        }
      })

  // Features.
    $('.features')
      .scrollex({
        mode: 'middle',
        top: '-20vh',
        bottom: '-20vh',
        initialize: function() {

          // Deactivate section.
            $(this).addClass('inactive');

        },
        enter: function() {

          // Activate section.
            $(this).removeClass('inactive');

        }
      });

  // FAQs

  var faq = document.getElementsByClassName("faq-page");
  var i;
  for (i = 0; i < faq.length; i++) {
      faq[i].addEventListener("click", function () {
        var a;
        for (a = 0; a < faq.length; a++) {
          if (this != faq[a]) {
            faq[a].parentNode.querySelectorAll(".faq-body")[0].classList.remove("show");
            faq[a].parentNode.querySelectorAll(".faq-page > .plus")[0].classList.remove("show");
          }
        }
        this.parentNode.querySelectorAll(".faq-body")[0].classList.toggle("show");
        this.parentNode.querySelectorAll(".faq-page > .plus")[0].classList.toggle("show");
      });
  }

  // Smooth scrolling

  const body = document.body;
  const main = document.getElementById('momentum-scroll');

  if (main != undefined) {

  let dy = 0;
  let prevdy = 0;
  let prev2dy = 0;

      var $a = $body.find('a');

      $a
        .addClass('scrolly')
        .on('click', function() {

          var $this = $(this);

          if ($this.attr('href') == undefined || $this.attr('href') == null || $this.attr('href') == "" || !$this.attr('href').startsWith("#")) {
            return;
          }

          scroll($this.attr('href').replace("#", ""))

        });

  function scroll(id) {

    let el = document.getElementById(id);

    for (var pos=0;el;el=el.offsetParent){
      pos +=  el.offsetTop-el.scrollTop;
    }

    window.scrollTo(0, pos);
  }

  body.style.height = main.clientHeight + 'px';
  main.style.top = 0;

  // Bind a scroll function
  window.addEventListener('mousewheel', easeScroll);

  function easeScroll() {
    sy = window.pageYOffset;
  }

  window.requestAnimationFrame(render);

  function render(){
    if (!browser.mobile) {
      dy = li(dy,window.pageYOffset,0.1);
    } else {
      dy = li(dy,window.pageYOffset,1);
    }
    dy = Math.floor(dy * 100) / 100;
    prev2dy = prevdy;
    prevdy = dy;
    
    main.style.transform = `translateY(-${dy}px)`;

    body.style.height = main.clientHeight + 'px';
    
    window.requestAnimationFrame(render);
  }

  function li(a, b, n) {
    return (1 - n) * a + n * b;
  }

}

  // Close the dropdown if the user clicks outside of it
  $window.on("click", function(event) {
    if (event.target.parentElement != null && !event.target.parentElement.classList.contains('dropdown')) {
      if (document.getElementsByClassName("dropdown-content")[0] != undefined && document.getElementsByClassName("dropdown-content")[0].classList.contains('show')) {
          document.getElementsByClassName("dropdown-content")[0].classList.remove('show');
      }
    }
  });

})(jQuery);

function showDropdown() {
  document.getElementsByClassName("dropdown-content")[0].classList.toggle("show");
}

function slide() {
  document.getElementsByClassName("right-arrow")[0].classList.toggle("show");
  document.getElementsByClassName("left-arrow")[0].classList.toggle("show");
  document.getElementsByClassName("column-left-content")[0].classList.toggle("show");
  document.getElementsByClassName("column-right-content")[0].classList.toggle("show");
}

function alert(error, title = "Whoops!") {
  document.querySelectorAll(".error-container > p")[0].innerHTML = error;
  document.querySelectorAll(".error-container > h2")[0].innerHTML = title;
  document.getElementsByClassName("error")[0].classList.add("show");
}

function closealert() {
  document.getElementsByClassName('error')[0].classList.remove('show');
  setTimeout(() => {document.querySelectorAll('.error-container > p')[0].innerHTML = 'Too fast! Slow down'}, 1000)
  setTimeout(() => {document.querySelectorAll('.error-container > h2')[0].innerHTML = 'Whoops!'}, 1000)
}

function report(element) {
  document.querySelectorAll(".rep-container > h2")[0].innerHTML = document.querySelectorAll(".rep-container > h2")[0].innerHTML + " " + element.parentElement.children[0].children[0].innerHTML;
  document.getElementsByClassName("rep")[0].classList.add("show");
}

function closereport() {
  document.querySelectorAll(".rep-container > h2")[0].innerHTML = "Report";
  document.getElementById('report-content').value = '';
  document.getElementsByClassName("rep")[0].classList.remove("show");
}

function discard(element) {
  document.querySelectorAll(".rep-container")[1].children[0].innerHTML = document.querySelectorAll(".rep-container > h2")[1].innerHTML + " " + element.parentElement.children[0].children[0].innerHTML + "?";
  document.getElementsByClassName("rep")[1].classList.add("show");
}

function closediscard() {
  document.querySelectorAll(".rep-container")[1].children[0].innerHTML = "Discard poll";
  document.getElementsByClassName("rep")[1].classList.remove("show");
}

function confirmdiscard(element) {
  let id = parseInt(element.parentElement.children[0].innerHTML.split("Discard poll #")[1].split("?")[0]);
  document.getElementsByClassName("rep")[1].classList.remove("show");
  $.post("/discard", {"address": address, "access_token": localStorage.getItem(address), "id": id}, (result) => {
    if (result !== true) {
      alert(result, "Discard failed..");
      return;
    } else {
      alert("Poll has been successfully discarded", "Discard success!");
      window.setTimeout(function () {
        location.reload();
      }, 2000);
    }
  });
}

function sendreport(element) {
  let id = parseInt(element.parentElement.children[0].innerHTML.split("Report #")[1]);
  let content = element.parentElement.children[1].value;
  if (content.length < 4 || content.length > 50) {
    alert("Reason must be between 4 to 50 characters");
    return;
  }
  document.getElementsByClassName("rep")[0].classList.remove("show");
  $.post("/report", {"address": address, "access_token": localStorage.getItem(address), "id": id, "content": content}, (result) => {
    if (result !== true) {
      document.getElementById('report-content').value = '';
      alert(result, "Report failed..");
      return;
    } else {
      alert("Report has been successfully filed", "Report success!");
    }
  });
}

async function checkWallet() {
  if (document.getElementById("v") == null) {
    if (web3Modal.cachedProvider == '') {
      return;
    }
    window.provider = await web3Modal.connect();
    web3 = new Web3(provider);
    var account = (await web3.eth.getAccounts())[0];
    if (account != undefined && document.getElementById("connect") != null) {
      document.getElementById("connect").innerHTML = account.slice(0, 5) + "..." + account.slice(-4) + "\nDisconnect";
    }
    if (await web3.eth.net.getNetworkType() != "main") {
      alert("Your wallet is on the Testnet.", "Warning");
      return;
    }
  }
}

async function disconnect(b = true) {
  window.provider = await web3Modal.connect();
  web3 = new Web3(provider);
  account = (await web3.eth.getAccounts())[0];
  await web3Modal.clearCachedProvider();
  window.provider = undefined;
  try {
    document.getElementById("connect").innerHTML = "Connect Wallet";
  } catch {}
  if (b) {
    window.location = "/";
  }
  localStorage.removeItem(account);
  alert("Wallet disconnected", "Success");
  return;
}

async function connectWallet() {

  if (web3Modal.cachedProvider != '') {
    await disconnect(false);
    return;
  }
  try {
    window.provider = await web3Modal.connect();
  } catch {
    alert("Failed to connect wallet, did you cancel it?");
    return;
  }
  web3 = new Web3(provider);
  if (await web3.eth.net.getNetworkType() != "main") {
    alert("Your wallet is on the Testnet!\nReconnect using the Mainnet!");
    return;
  }
  account = (await web3.eth.getAccounts())[0];
  if (account == undefined) {
    alert("Failed to connect wallet, no accounts selected.");
    return;
  }
  document.getElementById("connect").innerHTML = account.slice(0, 5) + "..." + account.slice(-4) + "\nDisconnect";
  alert("Wallet connected!", "Success");
}

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

async function gotoDashboard() {
  if (web3Modal.cachedProvider == '' || window.provider == undefined) {
    alert("You have to connect to your wallet first! Click the dashboard icon on the top right corner");
    return;
  } else {
    window.provider = await web3Modal.connect();
    web3 = new Web3(provider);
    document.getElementById("transition").classList.add("white");
    if (localStorage.getItem((await web3.eth.getAccounts())[0]) != null) {
      $.redirectPost("/dashboard", {'account': (await web3.eth.getAccounts())[0], 'access_token': localStorage.getItem((await web3.eth.getAccounts())[0])});
      return;
    }

    window.setTimeout(function () {
      window.location = "/verify?loc=dashboard";
    }, 1000);
  }
}

async function verify() {
  if (document.getElementById("v") != null) {
    window.provider = await web3Modal.connect();
    web3 = new Web3(provider);
    async function inner() {
      try {
        account = (await web3.eth.getAccounts())[0];
        if (account == undefined) {
          document.getElementById("transition").classList.add("white");

          window.setTimeout(async function () {
            await web3Modal.clearCachedProvider();
            window.provider = undefined;
            window.location = "/";
          }, 1000);
          return;
        }
        window.setTimeout(async function () {
          await inner();
        }, 1000);
      } catch {
        document.getElementById("transition").classList.add("white");

        window.setTimeout(async function () {
          await web3Modal.clearCachedProvider();
          window.provider = undefined;
          window.location = "/";
        }, 1000);
        return;
      }
    }
    await inner();
    return;
  }
}

