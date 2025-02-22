
function decrement() {
	document.getElementById("quantity").value = parseInt(document.getElementById("quantity").value) + ((parseInt(document.getElementById("quantity").value) > 1) ? -1 : 0);
}

function increment() {
	document.getElementById("quantity").value = parseInt(document.getElementById("quantity").value) + ((parseInt(document.getElementById("quantity").value) < 2000) ? 1 : 0);
}

function countdown() {
  let time = 1654250400 - Math.floor(Date.now() / 1000);
  if (time > 0) {
    let d = Math.floor(time / (3600*24));
    let h = Math.floor(time % (3600*24) / 3600);
    let m = Math.floor(time % 3600 / 60);
    let s = Math.floor(time % 60);

    document.getElementById("days").children[0].innerHTML = d;
    document.getElementById("hours").children[0].innerHTML = h;
    document.getElementById("minutes").children[0].innerHTML = m;
    document.getElementById("seconds").children[0].innerHTML = s;
  } else {
    document.getElementById("days").children[0].innerHTML = 0;
    document.getElementById("hours").children[0].innerHTML = 0;
    document.getElementById("minutes").children[0].innerHTML = 0;
    document.getElementById("seconds").children[0].innerHTML = 0;
    document.getElementById("days").style.background = `rgba(200,20,20,0.3)`;
    document.getElementById("hours").style.background = `rgba(200,20,20,0.3)`;
    document.getElementById("minutes").style.background = `rgba(200,20,20,0.3)`;
    document.getElementById("seconds").style.background = `rgba(200,20,20,0.3)`;
    document.getElementById("status").innerHTML = "Presale";
    document.getElementById("mint").setAttribute("onclick", "mint()");
  }
}

setInterval(countdown, 1000);

async function mint() {
	window.provider = await web3Modal.connect();
    web3 = new Web3(provider);
    var account = (await web3.eth.getAccounts())[0];
	$.post('/mint', {"address": account, "amount": parseInt(document.getElementById("quantity").value)}, async (result) => {
		const contract = new web3.eth.Contract(result.abi, result.address);
		function getErrorMessage(err) {
			try {
				err = result.errors[parseInt(err.message.split("execution reverted: ")[1])];
				if (err == undefined || err == null) {
					return "Error.. Did you cancel the transaction?";
				}
				return err;
			} catch {
				return "Error.. Did you cancel the transaction?";
			}
		}
		alert("Please do not click anything until the transaction completes", "Please wait");
		let res = await contract.methods.mint(parseInt(document.getElementById("quantity").value), result.proof).send({from: account, value: result.value}).catch((err)=>{alert(getErrorMessage(err));return;});
		if (res != undefined) {
			alert("Check your Brain Juice in the dashboard!", "Mint successful!");
		}
	});
}
