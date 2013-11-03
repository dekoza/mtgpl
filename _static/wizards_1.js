Event.observe(window, 'load', SetupAdvertisements);

var originalCityValue = null;

function FocusMagicLocatorTextBox(event, control)
{
    if(originalCityValue == null)
    {
        originalCityValue = control.value;
    }
    
    if(control.value == originalCityValue)
    {
        control.value = '';
    }
}

function UnfocusMagicLocatorTextBox(event, control)
{
    if(control.value == '')
    {
        control.value = originalCityValue;
    }
}

var originalSearchTextBoxValue = null;

function FocusSearchTextBox(event, control)
{
    if(originalSearchTextBoxValue == null)
    {
        originalSearchTextBoxValue = control.value;
    }
    
    if(control.value == originalSearchTextBoxValue)
    {
        control.value = '';
    }
}

function UnfocusSearchTextBox(event, control)
{
    if(control.value == '')
    {
        control.value = originalSearchTextBoxValue;
    }
}

function SetupAdvertisements()
{
    var topAdvertisementContainer = $('topAdvertisement');
    var rightAdvertisementContainer = $('rightAdvertisement');
    var articleAdvertisementContainer = null;
    // Un-comment this line to enable in-article advertisements.
    var articleAdvertisementContainer = $('articleAdvertisement');
    var articleFooterBanner = $('footerbanner');
    
    if(topAdvertisementContainer != null && rightAdvertisementContainer != null)
    {
        var topAdvertisement = new Element('iframe', { src: '/Magic/Advertisements/HorizontalAdvertisement.html?date=' + new Date().getTime(), frameborder: '0' });
        var rightAdvertisement = new Element('iframe', { src: '/Magic/Advertisements/VerticalAdvertisement.html?date=' + new Date().getTime(), frameborder: '0' });
        
        topAdvertisementContainer.update(topAdvertisement);
        rightAdvertisementContainer.update(rightAdvertisement);
    }

    if (articleAdvertisementContainer != null) {
    	var style = 'height:250px; width:300px; padding:0px; margin:0px; overflow:hidden; border:none; background:transparent;';

    	var articleAdvertisement = new Element('iframe', { src: '/Magic/Advertisements/ArticleAdvertisement.html?date=' + new Date().getTime(), frameborder: '0', 'style': style });

    	articleAdvertisementContainer.update(articleAdvertisement);
    }

    if (articleFooterBanner != null) {
        var footer = new Element('div');
        new Ajax.Request('/handlers/cmsservice.ashx?name=mtg_footer_banner_index',
            {
                method: 'get',
                onSuccess: function (transport) { 
                    var data = transport.responseText.evalJSON();
                    footer.innerHTML = data.BodyMarkup;
                }
            });
        articleFooterBanner.update(footer);
    }

    DoAdRotations();
}


function DoAdRotations() {
	// Randomly display one ad within every ad rotator on the page.
	// <show> tags within <adrotator> tags are rendered by XSL as hidden <div> tags. 
	// This function randomly un-hides one div from each ad rotator.  
	
	var allDivs = document.getElementsByTagName("div");
	for (var iDiv = 0; iDiv < allDivs.length; iDiv++) {
		// find the ad rotators
		var div = allDivs[iDiv];
		if (div.attributes.getNamedItem("adrotator")) {
			// find the ads within the rotator
			var nodes = div.getElementsByTagName("div");
			var ads = new Array();
			for (iNode = 0; iNode < nodes.length; iNode++) {
				if (nodes[iNode].attributes["ad"]) {
					ads.push(nodes[iNode]);
				}
			}
			// unhide a random ad
			var r = Math.floor(Math.random() * (ads.length));
			if (r < ads.length) {
				ads[r].style.display = "block";
			}
		}
	}
}


// configuration for autocard links via javascript
var gathererBaseURL = "http://gatherer.wizards.com";
//var gathererBaseURL = "qagatherer.wizards.com";
var expCodeLookup = {
    ARB: "Alara Reborn",
    CON: "Conflux",
    ALA: "Shards of Alara",
    EVE: "Eventide",
    SHA: "Shadowmoor",
    MOR: "Morningtide",
    LRW: "Lorwyn",
    FUT: "Future Sight",
    PLC: "Planar Chaos",
    TSB: "Time Spiral \"Timeshifted\"",
    TSP: "Time Spiral",
    DIS: "Dissension",
    GPT: "Guildpact",
    RAV: "Ravnica",
    SOK: "Saviors of Kamigawa",
    BOK: "Betrayers of Kamigawa",
    CHK: "Champions of Kamigawa",
    "5DN": "Fifth Dawn",
    DST: "Darksteel",
    MRD: "Mirrodin",
    SCG: "Scourge",
    LGN: "Legions",
    ONS: "Onslaught",
    JUD: "Judgment",
    TOR: "Torment",
    OD: "Odyssey",
    AP: "Apocalypse",
    PS: "Planeshift",
    IN: "Invasion",
    PR: "Prophecy",
    NE: "Nemesis",
    MM: "Mercadian Masques",
    CG: "Urza's Destiny",
    GU: "Urza's Legacy",
    UZ: "Urza's Saga",
    EX: "Exodus",
    ST: "Stronghold",
    TE: "Tempest",
    WL: "Weatherlight",
    VI: "Visions",
    MI: "Mirage",
    AL: "Alliances",
    CSP: "Coldsnap",
    IA: "Ice Age",
    HM: "Homelands",
    FE: "Fallen Empires",
    DK: "The Dark",
    LE: "Legends",
    AQ: "Antiquities",
    AN: "Arabian Nights",
    M10: "Magic 2010",
    "10E": "Tenth Edition",
    "9ED": "Ninth Edition",
    "8ED": "Eighth Edition",
    "7E": "Seventh Edition",
    "6E": "Classic Sixth Edition",
    "5E": "Fifth Edition",
    "4E": "Fourth Edition",
    "3E": "Revised Edition",
    "2U": "Unlimited Edition",
    "2E": "Limited Edition Beta",
    "1E": "Limited Edition Alpha"
};

// display popup based on the attributes of the caller <a> tag
function autoCardWindow(obj) {
	agent = navigator.userAgent;
	windowName = "Sitelet";
	params = "";
	params += "toolbar=1,";
	params += "location=1,";
	params += "directories=0,";
	params += "status=0,";
	params += "menubar=0,";  
	params += "scrollbars=1,";
	params += "resizable=1,";
	params += "width=800,";
	params += "height=670";

	// search by card name if non-numeric, multiverseId if numeric
	var keyName = obj.getAttribute("keyName");
	var keyValue = obj.getAttribute("keyValue");
	keyValue = keyValue.replace(/_/g, " ").replace(/\]/g, "&").replace(/\[/g, "'");

	// for split cards use first name only
	var iSlash = keyValue.indexOf(" // ");
	if (iSlash != -1) {
		keyValue = keyValue.substr(0, iSlash);
	}

	var options = ""; 
	if (obj.getAttribute("set")) {
		options += "&set=" + obj.getAttribute("set");
	}

	if (options && obj.getAttribute("lang")) {
		options += "&language=" + obj.getAttribute("lang");
	}

	var windowUrl = gathererBaseURL;
	var clickAction = obj.getAttribute("action");

	if (clickAction == "search" && obj.getAttribute("set")) {
		windowUrl += "/Pages/Search/Default.aspx?" + keyName + "=+[\"" + keyValue + "\"]&set=|[\"" + lookupSet + "\"]";
	} else {
		// get one or both card identifiers
		var ch = String.fromCharCode(31);
		keyValue = keyValue.replace("**", ch).replace("++", ch);
		var keys = keyValue.split(ch);

		if (keys.length > 1) {
			// two cardnames; search for both of them
			windowUrl += "/Pages/Search/Default.aspx?" + keyName + "=|[\"" + keys[0] +"\"]|[\"" + keys[1] + "\"]";
		} else {
			windowUrl += "/Pages/Card/Details.aspx?" + keyName + "=" + keyValue + options;
		}
	}
	var win = window.open(windowUrl, windowName, params);
}

// DG: remove?
function autoCardWindow3(cardname, set, border) 
{
    agent = navigator.userAgent;

    windowName = "Sitelet";

    params  = "";
    params += "toolbar=1,";
    params += "location=1,";
    params += "directories=0,";
    params += "status=0,";
    params += "menubar=0,";
    params += "scrollbars=0,";
    params += "resizable=0,";
    params += "width=232,";
    params += "height=317";

    win = window.open("/magic/card.asp?name="+cardname+"&set="+set+"&border="+border, windowName, params);

    if (!win.opener) 
    {
        win.opener = window;
    }
}

function makeWinXY(url, nWidth, nHeight) 
{  
  agent = navigator.userAgent;

  windowName = "xywindow";

  params  = "";
  params += "toolbar=0,";
  params += "location=0,";
  params += "directories=0,";
  params += "status=0,";
  params += "menubar=0,";
  params += "scrollbars=1,";
  params += "resizable=1,";
  params += "width=" + nWidth + ",";
  params += "height=" + nHeight;
  win = window.open(url, windowName , params);

  if (agent.indexOf("Mozilla/2") != -1 && agent.indexOf("Win") == -1) 
  {
      win = window.open(url, windowName , params);
  }

  if (!win.opener) 
  {
      win.opener = window;
  }
}

// DG: TODO:
function SubmitForm(event, control, formid, action)
{
	control.disabled = true;
	
	var formService = '/Handlers/FormService.ashx';
	
	var form = $(formid);
	
	if(form != null)
    {
        var inputs = form.select('input');
        var formParams = new Hash();
        
        for(var i = 0; i < inputs.length; i++)
        {
            var input = inputs[i];
            if(input.type == "checkbox")
            {
				if(input.checked)
				{
					formParams.set('formparam' + input.name, input.value);
				}
            }
            else if (input.type == "radio") {
                if (input.checked) {
                    formParams.set('formparam' + input.name, input.value);
                }
            }
			else
			{
				formParams.set('formparam' + input.name, input.value);
			}
        }
        formParams.set('formparamformname', formid);
        formParams.set('formparamurl', action);
	
		new Ajax.Request(formService, {
		        method: 'post',
			    parameters: formParams.toQueryString(),
			    onSuccess: function(transport) 
			    {
					control.disabled = false;
					
					window.location = transport.responseText;
			    }
			}
		);
	}
	
	
}

function SubmitPoll(event, control, pollid)
{
    control.disabled = true;
    
    var pollService = '/Handlers/PollService.ashx';
    
    var form = $(pollid);
    
    if(form != null)
    {
        var inputs = form.select('input');
        var selects = form.select('select');
        var pollParams = new Hash();
        
        for(var i = 0; i < inputs.length; i++)
        {
            var input = inputs[i];
            
            if(input.name == 'yn')
            {
                if(input.checked)
                {
                    pollParams.set('pollparam' + input.name, input.value);
                }
            }
            else
            {
                pollParams.set('pollparam' + input.name, input.value);
            }
        }
        
        for(var i = 0; i < selects.length; i++)
        {
            var select = selects[i];
            
            pollParams.set('pollparam' + select.name, select.value);
        }
        
        new Ajax.Request(pollService, {
		        method: 'post',
			    parameters: pollParams.toQueryString(),
			    onSuccess: function(transport)
			    {
			        var result = eval("(" + transport.responseText + ")");
			        var resultArea = form.select('.pollsubmitresult')[0];			        			        
		        
			        if(result.Result)
			        {
    		            if(resultArea.innerHTML == '')
			            {
			                resultArea.update('Your vote has been recorded!');
			            }
			        }
			        else
			        {
			            if(result.Message != null)
			            {
			                resultArea.update(result.Message);
			            }
			            else
			            {
			                resultArea.update('There was a problem recording your vote.');
			            }
			        }
			        
			        resultArea.style.display = 'block';
			        
			        control.disabled = false;
			    }	
		    }
	    );	
    }
    
    return false;
}

function CardBlock(obj) {
	// a block of one or two cards to be displayed;
	// input obj's keyValue attribute can consist of one url, or two urls separated by "**" or "++"
	// returns an object consisting of:
	//		urls = an array of 1 or 2 image handler URLs, based on the calling object's keyName and keyValue attributes and optional others;
	//		options = rotate/format options if any
	
	var keyName = obj.getAttribute("keyName");
	var keyValue = obj.getAttribute("keyValue");
	this.imageUrl = obj.getAttribute("imageUrl");

	keyValue = keyValue.replace(/_/g, " ").replace(/\]/g, "&").replace(/\[/g, "'");

	// parse stValue into 1 or 2 values;
	// first convert ++ to a single char 31 (because it's a non-keybd char) so the split function can work;
	var ch = String.fromCharCode(31);
	keyValue = keyValue.replace("++", ch);
	this.urls = keyValue.split(ch);
	for (var i = 0; i < this.urls.length; i++) {
		var st = "?type=card";
		if (keyName == "MultiverseId") {
			var mvid = this.urls[i]
			if (mvid && !isNaN(mvid)) {
				st += "&MultiverseId=" + mvid;
			}
		}
		else {
			st += "&name=" + this.urls[i];
				
			// if we have a card name we can also specify a set and language
			if (obj.getAttribute("set")) {
				st += "&set=" + obj.getAttribute("set");
			}

			if (st && obj.getAttribute("lang")) {
				st += "&language=" + obj.getAttribute("lang");
			}
		}
		this.urls[i] = st;
	}
	
	// get options 
	var opt = "";
	if (obj.getAttribute("rotate")) {
		opt += obj.getAttribute("rotate") + ",";
		}
	if (obj.getAttribute("format")) {
		opt += obj.getAttribute("format") + ",";
	}
	this.options = "&options=" + opt.substr(0, opt.length - 1); 	// trim off trailing comma
}

function OpenTip(event, obj) {
	var control = Event.element(event);

	var card = new CardBlock(obj);

	var tipClass = "tip";
	var cardClass = "tipcard";

	if (isCardWide(card)) {
		cardClass += "wide";
	}

	if (isCardWide(card) || card.urls.length > 1) {
		tipClass += "wide";
	}

	if (isCardSideways(card)) {
		tipClass += "rotated";
		cardClass += "rotated";
	}

	// build the tip tag as a <div> containing one or two <img> tags
	var imageHandler = gathererBaseURL + "/Handlers/Image.ashx"; // gatherer.wizards.com/Handlers/Image.ashx';
	// src can be an image url, cardname or mvid; if it's an url there is only one
	var imgSrc;
	if (card.imageUrl != null) {
		imgSrc = card.imageUrl;
	}
	else {

        if(card.urls[0].indexOf("\"") != -1)
        {
            var str = card.urls[0];
            str = str.replace(/\"/g, "%22");

            imgSrc = imageHandler + str + card.options;
                            

        }
        else
        {
		    imgSrc = imageHandler + card.urls[0] + card.options;
        }
	}


	var tipTag = '<div class="' + tipClass + '"><img class="' + cardClass + '" src="' + imgSrc + '" />';
	if (card.urls.length > 1) {
		// add the second image and widen the window;
		tipTag += '<img class="' + cardClass + '" src="' + imageHandler + card.urls[1] + card.options + '" />';
	}
	tipTag += "</div>";

	var tipWidth = 235;
	if (tipClass == "tipwide") { 
		tipWidth = 456;
	}
	else if (tipClass == "tiprotated" || tipClass == "tipwiderotated") {
		tipWidth = 320;
	}

	// open a popup window containing the tip tag
	var tip = new Tip(control, tipTag, {
        delay: .25,
        stem: 'topLeft',
        hook: { tip: 'topLeft', mouse: true }, 
        offset: { x: 10, y: 10 },
        border: 2,
        radius: 2,
        width: tipWidth
       });
	
}

function replaceAll(find, replace, str) {
  return str.replace(new RegExp(find, 'g'), replace);
}

function makeImageElement(srcUrl, cssClass) {
	// create an image element
	var img = document.createElement("img");
	img.src = srcUrl;
	img.className = cssClass;
	return img;
}

function isCardSideways(card) {
	return (card.options.indexOf("rotate90", 0) > 0 || card.options.indexOf("rotate270", 0) > 0);
}

function isCardWide(card) {
	return (card.options.indexOf("plane") > 0);
}

function ChangeBigCard(imageContainerId, obj) {
	// change a bigcard image's URL using attributes of obj
	var div = $('bigcard_' + imageContainerId);
	// remove existing images from div
	while (div.hasChildNodes()) {
		div.removeChild(div.lastChild);
	}

	var card = new CardBlock(obj);

	var deckClass = "mtgbigcard sidedeck";
	var cardClass = "sidedeckcard";

	if (isCardWide(card)) {
		cardClass += "wide";
	}

	if (isCardWide(card) || card.urls.length > 1) {
		deckClass += "wide";
	}

	if (isCardSideways(card)) {
		deckClass += "rotated";
		cardClass += "rotated";
	}

	var imageHandler = gathererBaseURL + "/Handlers/Image.ashx"; // gatherer.wizards.com/Handlers/Image.ashx';
	var imgSrc;
	if (card.imageUrl != null) {
		imgSrc = card.imageUrl;
	}
	else 
    {
        if(card.urls[0].indexOf("\"") != -1)
        {
            var str = card.urls[0];
            str = str.replace(/\"/g, "%22");

            imgSrc = imageHandler + str + "&size=small" + card.options;
        }
        else
        {
		    imgSrc = imageHandler + card.urls[0] + "&size=small" + card.options;
        }
	}

	var img = makeImageElement(imgSrc, cardClass);
	div.appendChild(img);
	// add second card mage if any
	if (card.urls.length > 1) {
		img = makeImageElement(imageHandler + card.urls[1] + card.options + "&size=small", cardClass);
		div.appendChild(img);
	}

	div.className = deckClass;
}

function ShiftCard(cardbox, shift) {
	// Cardbox is a div that contains two or three cards: a main card and alternate, or a main card, cardback, and alternate.
	// Cardbox is contained in a "revealer" div that is only one or two cards wide, which keeps one of the cards in cardbox hidden.
	// Mouseover/mouseout brings a different card into view by repositioning cardbox horizontally (or vertically of rotated).
	var newClass = cardbox.className.replace(" shiftleft", "").replace(" shiftup", "");
	if (shift == true) {
		if (newClass.indexOf("-rotated") >= 0) {
			newClass += " shiftup";
		} else {
			newClass += " shiftleft";
		}
	}
	cardbox.className = newClass;
}

// attempt to get the Width of a style selector from the page stylesheet ------ not used, doesn't work ------
function getCssValue(selector, attribute) {
	selector = selector.toLowerCase();
	var stylesheet;
	for (var nsheet = 0; nsheet < document.styleSheets.length; nsheet++) {
		stylesheet = document.styleSheets[nsheet];
		var n = stylesheet.cssRules.length;
		for (var i = 0; i < n; i++) {
			var selectors = stylesheet.cssRules[i].selectorText.toLowerCase().split(",");
			var m = selectors.length;
			for (j = 0; j < m; j++) {
				var sel = selectors[j].trim();
				if (selectors[j].trim() == selector) {
					var value = stylesheet.cssRules[i].style.getPropertyValue(attribute);
					if (value != "") {
						return value;
					}
				}
			}
		}
	}
	return null;
}


// Store locator widget
function miniloc_mouseover() {
	$('minilof_buttonactive').show();
	$('minilof_buttonstatic').hide();
}

function miniloc_mouseout() {
	$('minilof_buttonactive').hide();
	$('minilof_buttonstatic').show();
}

function miniloc_textbox_click() {
	var v = $('miniloc_text').value;
}

function miniloc_textbox_blur() {
	var v = $('miniloc_text').value;
	if (v == '')
	{ }
}

function miniloc_buttonclick(isNewWindow, opisparam) {
	var v = $('miniloc_text').value;

	var opis = opisparam;

	if (opis == '')
		opis = "1%3A222%2C1%3A224%2C1%3A217%3B1%3A216%2C1%3A45%2C1%3A57%3B1%3A234%2C1%3A57%3B1%3A9%3B1%3A150%2C1%3A151%2C1%3A152%2C1%3A155%2C1%3A156%2C1%3A157%2C1%3A158%2C1%3A159%3B1%3A229%2C1%3A230%3B1%3A133%2C1%3A25%2C1%3A201%2C1%3A197%2C1%3A150%2C1%3A194%2C1%3A198%2C1%3A56%2C1%3A158%2C1%3A199%2C1%3A11%3B";


	//var defaultOpis = "1%3A9";

	if (v != null) {
		v = v.strip();

		if (v != '') {
			var url = 'http://ww2.wizards.com/StoreAndEventLocator/Default.aspx?link=true' + '%26ReturnParamMapZoom=10%26ReturnParamMapSearch=' + v + '%26ReturnParamMode=play%26ReturnParamCheckedProducts=Magic%3A%20The%20Gathering%3BD%26D%3BAxis%20%26%20Allies%2CAxis%20%26%20Allies%20Miniatures%3B' + '%26ReturnParamCheckedEvents=' + opis + '%26ReturnParamCheckedEventBrands=1%3Ax%3B%26ReturnParamTablePage=0%26ReturnParamLastDirectionsQuery=null';
			//var url = 'http://ww2.wizards.com/StoreAndEventLocator/Default.aspx?link=true' + '%26ReturnParamMapZoom=10%26ReturnParamMapSearch=' + v + '%26ReturnParamMode=play%26ReturnParamCheckedProducts=Magic%3A%20The%20Gathering%3BD%26D%3BAxis%20%26%20Allies%2CAxis%20%26%20Allies%20Miniatures%3B' + '%26ReturnParamCheckedEvents=1%3A9' + '%26ReturnParamCheckedEventBrands=1%3Ax%3B%26ReturnParamTablePage=0%26ReturnParamLastDirectionsQuery=null';                        
			url = url.replace(/%26/g, String.fromCharCode(38));

			if (isNewWindow) {
				var newWindow = window.open(url, '_blank');
				//newWindow.focus();
			}
			else {
				window.location.href = url;
			}
		}
	}
}






Event.observe(window, 'load', function() {

	if ($('miniloc_text') != null) {
		$('miniloc_text').observe('keypress', function(event) {
			if (event.keyCode == Event.KEY_RETURN) {
				miniloc_buttonclick(true, ''); Event.stop(event);
			}
		});
	}
});



function loadJSFile(fileName) {
  var jsFile = document.createElement('script');
  jsFile.setAttribute('type','text/javascript');
  jsFile.setAttribute('src', fileName);
  document.getElementsByTagName('head')[0].appendChild(jsFile);
}

function loadCSSFile(fileName) {
  var cssFile = document.createElement('link');
  cssFile.setAttribute('rel', 'stylesheet');
  cssFile.setAttribute('type', 'text/css');
  cssFile.setAttribute('href', fileName);
  document.getElementsByTagName("head")[0].appendChild(cssFile);
}



Event.observe(window, 'load', function () {
    // faction leaderboard
    if ($('faction_leaderboard_wrapper') != null) {
        new Ajax.Request('/Handlers/FactionPWP.ashx',
        {
            method: 'get',
            parameters: { nocache:new Date().getTime()},
            onSuccess: function (transport) {
                var response = transport.responseText || "no response text";
                var data = eval('(' + response + ')');
                for(var i = 0; i < data.length; i++) {
                    var factionWrapper = document.createElement('div');
                    factionWrapper.addClassName('clan-display-class ' + data[i].FactionName + '-display-class');
                    var factionName = document.createElement('div');
                    factionName.addClassName('faction-leaderboard-faction-name');
                    factionName.update(data[i].FactionName);
                    var factionPWP = document.createElement('div');
                    factionPWP.addClassName('faction-leaderboard-pwp-score');
                    factionPWP.update(data[i].PWP);
                    var factionRank = document.createElement('div');
                    factionRank.addClassName('faction-leaderboard-rank');
                    factionRank.update(data[i].Rank);
                    factionWrapper.appendChild(factionName);
                    factionWrapper.appendChild(factionPWP);
                    factionWrapper.appendChild(factionRank);
                    $('faction_leaderboard_wrapper').appendChild(factionWrapper);
                }
            }
        });
    }

});

Event.observe(window, 'load', function () {
    // faction leaderboard score
    // faction leaderboard
    var factions = $$('div.faction_pwp_wrapper');
    if (factions != null) {
        factions.each(function(fact, index) {
            var classes = $w(fact.className);
            classes.each(function(clazz, clazzIndex) {
                if(clazz != 'faction_pwp_wrapper') {
                    new Ajax.Request('/Handlers/FactionPWP.ashx',
                    {
                        method: 'get',
                        parameters: { faction: clazz , nocache:new Date().getTime()},
                        ajaxMyFaction: fact,

                        onSuccess: function (transport) {
                            var response = transport.responseText || "no response text";
                            var data = eval('(' + response + ')');
                            data.each(function(e) {
                                var factionWrapper = document.createElement('div');
                                factionWrapper.addClassName('clan-display-class ' + e.FactionName + '-display-class');
                                var factionName = document.createElement('div');
                                factionName.addClassName('faction-leaderboard-faction-name');
                                factionName.update(e.FactionName);
                                var factionPWP = document.createElement('div');
                                factionPWP.addClassName('faction-leaderboard-pwp-score');
                                factionPWP.update(e.PWP);
                                var factionRank = document.createElement('div');
                                factionRank.addClassName('faction-leaderboard-rank');
                                factionRank.update(e.Rank);
                                factionWrapper.appendChild(factionName);
                                factionWrapper.appendChild(factionPWP);
                                factionWrapper.appendChild(factionRank);
                                fact.appendChild(factionWrapper);
                            });
                        }
                    });
                }
            });
        });
    }
});




