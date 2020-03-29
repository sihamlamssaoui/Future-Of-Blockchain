function getParams(params) {
    let method = params.method;
    let depositGuest = params.depositGuest ?  params.depositGuest : 10;
    let depositHost = params.depositHost ?  params.depositHost : 10;
    let price = params.price ?  params.price : 30;
    let cp = params.cp ?  params.cp : 0;
   
    return `{  "prim": "Pair",  "args": [    {      "prim": "Pair",      "args": [        
        { "prim": "Pair", "args": [ { "int": "${cp}" }, { "int": "${depositGuest}" } ] },        
        { "prim": "Pair", "args": [ { "string": "tz1hrA5ZBXTjwEXcd8x1Q5sLtEaANNeMwZzN" }, 
        { "int": "${depositHost}" } ] }      ]    },    {      "prim": "Pair",      "args": [        
        { "prim": "Pair", "args": [ { "string": "tz1bDQiy4CCnMDnKvWzNixZJDQtXEnFJu4GB" }, 
        { "string": "${method}" } ] },        { "prim": "Pair", "args": [ 
        { "string": "tz1hqAAZY9rDgWKAZzXGQfzcqU1Uo97Z2rr7" }, { "int": "${price}" } ] } 
             ]    }  ]}`;
}

const contractAddress = 'KT18pDcpc91w9uyTASnECL911kyrJAW9XpcB';
const tezosNode = 'https://tezos-dev.cryptonomic-infra.tech/';
const paramFormat = conseiljs.TezosParameterFormat.Micheline;
const conseilServer = {
    url: 'https://conseil-dev.cryptonomic-infra.tech:443',
    apiKey: '8ed0e93a-9dce-4a72-9aa9-26cb69d111fb',
    network: 'carthagenet'
}
const networkBlockTime = 30 + 1;
const secretKey = 'edskRxaUY4jMNPLyCBREajKWwi88N4rLkpMWpCnfCFfKSf3ACnWWrLLNiULjH52V8om369r3AkFVLJ6asbfvnaRiZDw7UXDR7w';
const alphanetFaucetAccount = {
  "mnemonic": [
    "trouble",
    "blouse",
    "smile",
    "pull",
    "boring",
    "pepper",
    "fossil",
    "spike",
    "laptop",
    "taxi",
    "bag",
    "muffin",
    "under",
    "narrow",
    "lunar"
  ],
  "secret": "314838e9b570c6f03d81e9efc75afa307ba1b712",
  "amount": "6362274230",
  "pkh": "tz1auTWPGUKVYiXFPM6hKd1vvN1YP1UUjVMM",
  "password": "MraKWBZ6pi",
  "email": "dffryobo.mepfvkko@tezos.example.org"
};

function clearRPCOperationGroupHash(hash) {
    return hash.replace(/\"/g, '').replace(/\n/, '');
}

async function initAccount() {
    keyStore = await conseiljs.TezosWalletUtil.restoreIdentityWithSecretKey(secretKey);
}

async function makeRequest(params, keyStore, amount) {
    log('Sending...')
    $(".overly-loader").show()

    try {
        //await initAccount();
        let nodeResult = await nodeActivation(params, keyStore, amount);
        log("helooooooooooooooooooooooo");
        let groupid = clearRPCOperationGroupHash(nodeResult.operationGroupID);
        log(groupid)
        let conseilResult = await OperationConfirmation(groupid);
        log('Activation has been accepted, operation ID : ' + groupid);
        
        /*if (conseilResult.length == 1 && conseilResult[0]['status'] !== 'applied') {
            nodeResult = await conseiljs.TezosNodeReader.getBlock(tezosNode, conseilResult[0]['block_hash']);
            $(".overly-loader").hide()
            return false;
        }
        
        if (conseilResult.length == 1 && conseilResult[0]['status'] === 'applied') {
            conseilResult = await conseiljs.TezosConseilClient.getAccount(conseilServer, conseilServer.network, contractAddress);
            log('Request has been saved')
        }*/
        $(".overly-loader").hide()
    } catch (error) {
        alertBox('Something went wrong please try again: details: '+error)
        $(".overly-loader").hide()
    }
   
    return true
}

//  Button action
$(function () {
    // owner actions 
    $("#owner .contract-init").on('click', async function () {
        // Clear alerbox
        clearAlertBox()

        let price = $(".step-one .price", "#owner").val();
        let depositHost = $(".step-one .depositHost", "#owner").val();
        let depositGuest = $(".step-one .depositGuest", "#owner").val();
        let cp = $(".step-one .cp", "#owner").val();
        
        // Check if required values has been submited
        if(!price || !depositHost || ! depositGuest || !cp ){
            alertBox('All fields are required')
            return
        }
        
        if(parseFloat(price) == "NaN"){
          alertBox('Price must be a number')
            return false;
        }
        
         if(parseFloat(depositHost) == "NaN"){
          alertBox('Deposit host must be a number')
            return false;
        }
        
        if(parseFloat(depositGuest) == "NaN"){
          alertBox('Deposit guest must be a number')
            return false;
        }
        
        const keyStore = {
        publicKey: 'edpktzs89mf1SbPY5KKyuHNpcWpBEVsXhmYznDzfuA3XYjnBXghvRf',
        privateKey: 'edskRrDHYiccewDm1xDFeSTduuCDd4atEoPy5SS1GZJHrq6BC6ab1DM3MZA2kMCVWDMfwHJ2VVSmyhFjBAWkWmTVKgm4QmZ5s6',
        publicKeyHash: 'tz1bDQiy4CCnMDnKvWzNixZJDQtXEnFJu4GB',
        seed: '',
        storeType: conseiljs.StoreType.Fundraiser
        };
        
        // defined params on the getparams must be submitted here otherwise you will get error
        let params = { 'method': 'Contract_Initialisation',
                'price': price,
                'depositGuest': depositGuest,
                'depositHost': depositHost,
                'cp': cp
             }
        let amount = depositHost;
        // The makerequest must return true if everything is good otherwise it must return false      
        let request = await makeRequest(getParams(params), keyStore, amount);
        if ( request ) {
            // Hide all steps and show the next one
            $("#owner .step").hide();
            //$("#owner .step-two").show();

            // Disabled all buttons and enable the next one
            $("#owner .btn").prop('disabled', true);
            $("#owner .cancellation").prop('disabled', false);
        }
    });

   

    $("#owner .cancellation").on('click', async function () {
        log('cancel..')
        const keyStore = {
        publicKey: 'edpktzs89mf1SbPY5KKyuHNpcWpBEVsXhmYznDzfuA3XYjnBXghvRf',
        privateKey: 'edskRrDHYiccewDm1xDFeSTduuCDd4atEoPy5SS1GZJHrq6BC6ab1DM3MZA2kMCVWDMfwHJ2VVSmyhFjBAWkWmTVKgm4QmZ5s6',
        publicKeyHash: 'tz1bDQiy4CCnMDnKvWzNixZJDQtXEnFJu4GB',
        seed: '',
        storeType: conseiljs.StoreType.Fundraiser
        };
        const amount = 0;
         // defined params on the getparams must be submitted here otherwise you will get error
        let params = { 
            'method': 'Cancellation_Host'
        }

        // The makerequest must return true if everything is good otherwise it must return false  
        let request = await makeRequest(getParams(params), keyStore, amount);
        if ( request ) {
            // Hide all steps and show the next one
            $("#owner .step").show();

            // Disabled all buttons and enable the next one
            $("#owner .btn").prop('disabled', true);
            $("#owner .contract-init").prop('disabled', false);
        }
    });

    // visitor actions 
    

    $("#visitor .sendPrice").on('click', async function () {
        // Clear alerbox
        clearAlertBox()

        let price = $(".step-one .price", "#visitor").val();
        let depositGuest = $(".step-one .depositGuest", "#visitor").val();

        // Check if required values has been submited
        if(parseFloat(price) == "NaN"){
            alertBox('Price must be a number')
            return false;
        }
        // Check if required values has been submited
        if(parseFloat(depositGuest) == "NaN"){
            alertBox('depositGuest must be a number')
            return false;
        }
        const keyStore = {
        publicKey: 'edpkuZeqZkobZGszh8SrHw2s1HR8dmU76a6c6mWMbZbMmzacFRVjm',
        privateKey: 'edskRhkGiPUM1G1Y7VS1RfZaP3vXo6XQ8Hb1Qbu8dGLJebwTvTqG3CH3KPVzyEq2LKYWnYNcHa2VwqDuFoKsMGEWLJncN9AUpK',
        publicKeyHash: 'tz1hrA5ZBXTjwEXcd8x1Q5sLtEaANNeMwZzN',
        seed: '',
        storeType: conseiljs.StoreType.Fundraiser
        };
        const amount = parseFloat(depositGuest) + parseFloat(price);
         // defined params on the getparams must be submitted here otherwise you will get error
        let params = { 
                'method': 'Send_Deposit_Guest',
                'price': price,
                'depositGuest': depositGuest
        }

        // The makerequest must return true if everything is good otherwise it must return false  
        let request = await makeRequest(getParams(params), keyStore, amount);
        if ( request ) {
            // Hide all steps and show the next one
            $("#visitor .step").hide();

            // Disabled all buttons and enable the next one
            $("#visitor .btn").prop('disabled', true);
            $("#visitor .Issues").prop('disabled', false);
            $("#visitor .cancellation").prop('disabled', false);
        }
        
    });
  
    /*  // visior issues unused code
        let noElec = $(".step-three .noElec", "#visitor").prop("checked");
        let noWater = $(".step-three .noWater", "#visitor").prop("checked");
        issuesit = $("theresIssues").prop("checked");
        // Check if required values has been submited
        if(issuesit){
            if(chkbox1 == false && chkbox2 == false){
                alertBox('you must select an issue')
                return false;
            }
        }

         // defined params on the getparams must be submitted here otherwise you will get error
        let params = { 
            'method': 'Issues',
                'noElec': noElec,
                'noWater': noWater
        }

        // The makerequest must return true if everything is good otherwise it must return false  
      let request = await makeRequest(params);
        if ( request ) {
            // Hide all steps and show the next one
            $("#visitor .step").hide();
            
            //$("#visitor .step-four").show();

            // Disabled all buttons and enable the next one
            $("#visitor .btn").prop('disabled', true);
            $("#visitor .renewContractBut").prop('disabled', false);
            $("#visitor .issueCancel").prop('disabled', false);
            $("#visitor .FinishContractVisitor").prop('disabled', false);
            $("#visitor .cancellation").prop('disabled', false);
        }*/
    
    $("#visitor .Issues").on('click', async function () {
        // Clear alerbox
        clearAlertBox();

        $("#visitor .step-three").toggle();
        $("#visitor .renewContractBut").prop('disabled', false);
        $("#visitor .issueCancel").prop('disabled', false);
        // The makerequest must return true if everything is good otherwise it must return false  
        
        const keyStore = {
        publicKey: 'edpkuZeqZkobZGszh8SrHw2s1HR8dmU76a6c6mWMbZbMmzacFRVjm',
        privateKey: 'edskRhkGiPUM1G1Y7VS1RfZaP3vXo6XQ8Hb1Qbu8dGLJebwTvTqG3CH3KPVzyEq2LKYWnYNcHa2VwqDuFoKsMGEWLJncN9AUpK',
        publicKeyHash: 'tz1hrA5ZBXTjwEXcd8x1Q5sLtEaANNeMwZzN',
        seed: '',
        storeType: conseiljs.StoreType.Fundraiser
        };
        const amount = 0;

        let request = await makeRequest(getParams(params), keyStore, amount);
        

        
    });
    
    
    $("#visitor .issueCancel").on('click', async function () {
        // Clear alerbox
        clearAlertBox()

         // defined params on the getparams must be submitted here otherwise you will get error
        let params = { 
            'method': 'Guest_Accepts_Refund'
        }
        const keyStore = {
        publicKey: 'edpkuZeqZkobZGszh8SrHw2s1HR8dmU76a6c6mWMbZbMmzacFRVjm',
        privateKey: 'edskRhkGiPUM1G1Y7VS1RfZaP3vXo6XQ8Hb1Qbu8dGLJebwTvTqG3CH3KPVzyEq2LKYWnYNcHa2VwqDuFoKsMGEWLJncN9AUpK',
        publicKeyHash: 'tz1hrA5ZBXTjwEXcd8x1Q5sLtEaANNeMwZzN',
        seed: '',
        storeType: conseiljs.StoreType.Fundraiser
        };
        const amount = 0;
        // The makerequest must return true if everything is good otherwise it must return false  
        let request = await makeRequest(getParams(params), keyStore, amount);
        if ( request ) {
            // Hide all steps and show the next one
            $("#visitor .step").hide();
            $("#visitor .step-one").show();

            // Disabled all buttons and enable the next one
            $("#visitor .btn").prop('disabled', true);
            $("#visitor .sendPrice").prop('disabled', false);
        }
    });
    
    
    $("#visitor .renewContractBut").on('click', async function () {
        // Clear alerbox
        clearAlertBox()

         // defined params on the getparams must be submitted here otherwise you will get error
        let params = { 
            'method': 'Guest_Leaves_Contract'
        }
        const keyStore = {
        publicKey: 'edpkuZeqZkobZGszh8SrHw2s1HR8dmU76a6c6mWMbZbMmzacFRVjm',
        privateKey: 'edskRhkGiPUM1G1Y7VS1RfZaP3vXo6XQ8Hb1Qbu8dGLJebwTvTqG3CH3KPVzyEq2LKYWnYNcHa2VwqDuFoKsMGEWLJncN9AUpK',
        publicKeyHash: 'tz1hrA5ZBXTjwEXcd8x1Q5sLtEaANNeMwZzN',
        seed: '',
        storeType: conseiljs.StoreType.Fundraiser
        };
        const amount = 0;
        // The makerequest must return true if everything is good otherwise it must return false  
        let request = await makeRequest(getParams(params), keyStore, amount);
        if ( request ) {
            // Hide all steps and show the next one
            $("#visitor .step").hide();
            $("#visitor .step-one").show();

            // Disabled all buttons and enable the next one
            $("#visitor .btn").prop('disabled', true);
            $("#visitor .sendPrice").prop('disabled', false);
        }
            
    });
    

    $("#visitor .cancellation").on('click', async function () {

        // Clear alerbox
        clearAlertBox()

        
         // defined params on the getparams must be submitted here otherwise you will get error
        let params = { 
            'method': 'Cancellation_Guest'
        }
        const keyStore = {
        publicKey: 'edpkuZeqZkobZGszh8SrHw2s1HR8dmU76a6c6mWMbZbMmzacFRVjm',
        privateKey: 'edskRhkGiPUM1G1Y7VS1RfZaP3vXo6XQ8Hb1Qbu8dGLJebwTvTqG3CH3KPVzyEq2LKYWnYNcHa2VwqDuFoKsMGEWLJncN9AUpK',
        publicKeyHash: 'tz1hrA5ZBXTjwEXcd8x1Q5sLtEaANNeMwZzN',
        seed: '',
        storeType: conseiljs.StoreType.Fundraiser
        };
        const amount = 0;
        // The makerequest must return true if everything is good otherwise it must return false  
        let request = await makeRequest(getParams(params), keyStore, amount);
        if ( request ) {
            // Hide all steps and show the next one
            $("#visitor .step").hide();
            $("#visitor .step-one").show();

            // Disabled all buttons and enable the next one
            $("#visitor .btn").prop('disabled', true);
            $("#visitor .sendPrice").prop('disabled', false);

        }
    });



    $("#nuki .nukiBtn").on('click', async function () {

        // Clear alerbox
        clearAlertBox()

        
         // defined params on the getparams must be submitted here otherwise you will get error
        let params = { 
            'method': 'Door_Opened'
        }
        const keyStore = {
        publicKey: 'edpktfDnCBRqj2vVvagPjqKWUH8jYJuKPK69Ra7xa1ZtLRzux3SUX',
        privateKey: 'edskRt7Tq4zeRyyBWeYfPxBme3eLyumAutcxmJEvUBHKvM8UGoMsJ6dX9N1s39xLjMNhoLkteBDMfxVb1RZb5UikQLeXyyJr6a',
        publicKeyHash: 'tz1hqAAZY9rDgWKAZzXGQfzcqU1Uo97Z2rr7',
        seed: '',
        storeType: conseiljs.StoreType.Fundraiser
        };
        const amount = 0;
        // The makerequest must return true if everything is good otherwise it must return false  
        let request = await makeRequest(getParams(params), keyStore, amount);
        if ( request ) {
            // Disabled all buttons and enable the next one
            $("#nuki .btn").prop('disabled', true);
            $("#nuki .nukiEnd").prop('disabled', false);

        }
    });

    $("#nuki .nukiEnd").on('click', async function () {

        // Clear alerbox
        clearAlertBox()

        
         // defined params on the getparams must be submitted here otherwise you will get error
        let params = { 
            'method': 'End_Of_Rent'
        }
        const keyStore = {
        publicKey: 'edpktfDnCBRqj2vVvagPjqKWUH8jYJuKPK69Ra7xa1ZtLRzux3SUX',
        privateKey: 'edskRt7Tq4zeRyyBWeYfPxBme3eLyumAutcxmJEvUBHKvM8UGoMsJ6dX9N1s39xLjMNhoLkteBDMfxVb1RZb5UikQLeXyyJr6a',
        publicKeyHash: 'tz1hqAAZY9rDgWKAZzXGQfzcqU1Uo97Z2rr7',
        seed: '',
        storeType: conseiljs.StoreType.Fundraiser
        };
        const amount = 0;
        // The makerequest must return true if everything is good otherwise it must return false  
        let request = await makeRequest(getParams(params), keyStore, amount);
        if ( request ) {
            // Disabled all buttons and enable the next one
            $("#nuki .btn").prop('disabled', true);
            $("#nuki .nukiBtn").prop('disabled', false);

        }
    });


});

async function nodeActivation(params, keyStore, amount){  
    console.log("hello");
    let result = await conseiljs.TezosNodeWriter.sendContractInvocationOperation(tezosNode, keyStore, contractAddress, amount, 500000, '', 1000, 750000, undefined, params, paramFormat);
    return result;
}

async function OperationConfirmation(groupid){
  let result = await conseiljs.TezosConseilClient.awaitOperationConfirmation(conseilServer, conseilServer.network, groupid, 5);
  console.log('Greaaaaat');
  return result;
}

// Helpers 
// Alert box takes 2 params msg: text you want to display, type the alert type it must be (danger | warning | success | info)
function alertBox(msg, type) {
    if (!type) type = 'danger'
    $(".alert").addClass("alert-" + type).html(msg);
}

// show debug info
function log(msg) {
    if(!msg) return
    $(".debug").append("<div>"+msg+"</div>");
}

function clearAlertBox() {
    let ab = $(".alert");
    ab.html('');
    ab.removeClass();
    ab.addClass("alert");
}
