function getHiddenFieldVal(elemName) {
    var val;
    var elem = document.getElementsByName(elemName);
    if (elem) {
        val = (elem.length > 1) ? elem[0].value : elem.value;
    }
    return val;
}

function printfire()
{
    // Firefox
    if (document.createEvent && window.dispatchEvent) {
        printfire.args = arguments;
        var ev = document.createEvent("Events");
        ev.initEvent("printfire", false, true);
        window.dispatchEvent(ev);
    }
}
//This functions handle setting defaults for protein or nulcleotide suite  search page when
//one of blast program radio buttons is clicked - not used now
function AdjustMoreOptionsStyle()
{
	var optsEl = document.getElementById("moreopts");
	if(optsEl && optsEl.style.height != "0px") {
		optsEl.style.height = optsEl.scrollHeight + "px";
	}
}

//Strip (taxid:XXX) from organism list selection
//sgRunFunc="AdjustOrganism();"
function AdjustOrganism()
{
	var words = $("qorganism").value.split(" (taxid");
	$("qorganism").value = words[0];
}


/* JS Common to all BLAST pages */


function setResultsTarget()
{
	//var newWin = $("newwin");
	var newWin = this;
	var searchFrm = $(newWin.getAttribute("form"));
	if(newWin && newWin.checked == true) {
		if(newWin.getAttribute("winType") == "random") {
			searchFrm.target = "Blast_Results_for_" + Math.floor(Math.pow(10,10) *Math.random());
		}
		else {
			searchFrm.target = $("resPageTarget").value;
		}
	}
	else {
		searchFrm.target = "";
	}
}

function diffFromDefault(elem)
{
    var currentVal = "";
    var ret = 0;

    if (!(elem)) return;
    var defVal = elem.getAttribute("defVal"); //Default value
    if(elem.type == "select-multiple") {
        defVal = "";
    }
    var elShowDiff = utils.getParent(elem);
    if(!elem.type) {//div element for example
        //Check if parent elem has "hide" class
        if(utils.hasClass(utils.getParent(elem), "hide")) {
            currentVal = "hide";
        }
        else {
            currentVal = "show";
        }
        elShowDiff = elem;
    }
    else if (elem.type == "select-one") {
        var selIndex = elem.selectedIndex;
        if (selIndex >= 0 && elem[selIndex] && elem[selIndex].value) {
            currentVal = elem[selIndex].value;
        }
        //If Default value is not specified - the first one in the selection list is the default
        if (!defVal && elem[0].value) defVal = elem[0].value;
    }
    else if(elem.type == "select-multiple") {
	    currentVal = "";//for now
    }
    else if(elem.type == "checkbox") {
        //alert("defVal1=" + elem.id + " " + defVal);
        //var defVal = elem.defVal; //Default value
        //alert("defVal2=" + defVal);
        if(elem.checked == true) currentVal = "checked"
        else  currentVal = "unchecked";
    }
    else {
        currentVal = elem.value;
    }


    var numdiff = parseInt($("NUM_DIFFS").value,10);
    var optsNumDiff = parseInt($("NUM_OPTS_DIFFS").value,10);
    if(defVal != currentVal) {
        if(!utils.hasClass(elShowDiff, "nondef")) {
            utils.addClass(elShowDiff, "nondef");
            numdiff++;
            if(utils.hasClass(elem,"opts")) optsNumDiff++;
        }
        ret = 1;
    }
    else {
        if(utils.hasClass(elShowDiff, "nondef")) {
            utils.removeClass(elShowDiff, "nondef");
            //alert("noDiff-" + elem.id);
            if(numdiff != 0) numdiff--;
            if(utils.hasClass(elem,"opts")) optsNumDiff--;
        }
        ret=0;
    }
    $("NUM_DIFFS").value = numdiff;
    $("NUM_OPTS_DIFFS").value = optsNumDiff;
    if(numdiff > 0) {
        $("diffMes").style.display = "inline";
    }
    else {
        $("diffMes").style.display = "none";
    }
    //alert(elem.id + " " + $("NUM_DIFFS").value);
    return ret;
}

function setDefalValue(elem)
{
    var currentVal;
    var defVal = elem.getAttribute("defVal"); //Default value
    if(elem.type == "select-one") {
        //If Default value is not specified - the first one in the selection list is the default
        if(!defVal) defVal = elem[0].value;
        for(j=0; j < elem.options.length; j++) {
		    if(elem.options[j].value == defVal) {
		        elem.options[j].selected = true;
		        break;
		    }
        }
    }
    else if(elem.type == "checkbox" || elem.type == "radio") {
        if(!defVal) defVal = "checked";
        if(defVal == "checked") elem.checked = true
        else elem.checked = false;
    }
    else {
        if(!defVal) defVal = "";
        elem.value = defVal;
    }

    var elShowDiff = utils.getParent(elem);
    if(utils.hasClass(elShowDiff, "nondef")) {
        utils.removeClass(elShowDiff, "nondef");
    }
    //alert(elem.id + " " + $("NUM_DIFFS").value);
}

function newResultsWinInit() {
    jQuery("[class='newwin']").each(function(index) {
        utils.addEvent(this, "click", setResultsTarget, false);
    });
}

function bannerAdInit()
{
    jQuery("#banner_ad #closeAd").bind("click", function (e) {
        var ariaContrl = jQuery(this).attr("aria-controls");
        jQuery("#" + ariaContrl).remove();
        var pagetype = jQuery(this).attr("pagetype");
        var program = jQuery(this).attr("program");
        var blastspec = jQuery(this).attr("blastspec");
        if(pagetype || program || blastspec) {
            updateUserSurvey(pagetype,program,blastspec);
        }
    });
    jQuery("#banner_ad #jt").bind("click", function (e) {
        jQuery("#btnJt").click();
    });
    jQuery("#btnJt").bind("click", function(e) {
        winRef = window.open(jQuery("#jt")[0].href, "hlp" )
        jQuery("#closeAd").click();
    });
}

function resetOrganismSuggest(orgEntryElem)
{
    //suggestHint is in the hidden field used for SRA
    var defaultMessage = ($("suggestHint")) ? $("suggestHint").value : "Enter organism name or id--completions will be suggested";
    var suggestHint = $("qorganism").getAttribute("suggestHint");
    if(suggestHint) defaultMessage = suggestHint;
    if(orgEntryElem.value == "") {
        orgEntryElem.value = defaultMessage;
    }
    if(orgEntryElem.value == defaultMessage) {
        utils.addClass(orgEntryElem,"orgHint");
    }
}

function setupOrganismSuggest(orgEntryElem)
{
    resetOrganismSuggest(orgEntryElem);
    utils.addEvent(orgEntryElem, "focus", function() {
        clearOrgSuggest(orgEntryElem);
     }, false);
}

function clearOrgSuggest(orgEntryElem)
{
    if(utils.hasClass(orgEntryElem,"orgHint")) {
        orgEntryElem.value="";
        utils.removeClass(orgEntryElem,"orgHint");
    }
}

function InitCustomButton(bn)
{
  utils.addEvent(bn, "mouseover", function() {this.src = this.getAttribute("mouseovImg");}, false);
  utils.addEvent(bn, "mouseout", function() {this.src = this.getAttribute("mouseoutImg");}, false);
  utils.addEvent(bn, "mousedown", function() {this.src = this.getAttribute("mousedownImg");}, false);
  utils.addEvent(bn, "mouseup", function() {this.src = this.getAttribute("mouseupImg");}, false);
}

function showHideElem(id,hide)
{
  if($(id)) {
    if(hide) {
	    if(!utils.hasClass($(id),"hidden")) utils.addClass($(id), "hidden");
	}
	else {
	    if(utils.hasClass($(id),"hidden")) utils.removeClass($(id), "hidden");
	}
  }
}

function resetOrganismControls(orgEntryElem) {
    resetOrganismSuggest(orgEntryElem);
    var orgIDMod = jQuery(orgEntryElem).attr("idMod"); //"Exp"
    orgIDMod = (orgIDMod) ? orgIDMod : "";
    if ($("orgExcl" + orgIDMod)) $("orgExcl" + orgIDMod).checked = false;
    utils.replaceInHtml("", $("orgs" + orgIDMod));
    if ($("frOrgs")) utils.replaceInHtml("", $("frOrgs"));
    if ($("numOrg" + orgIDMod)) $("numOrg" + orgIDMod).value = 1;
}

//orgID is the id of original organism box (qorganism,qorganismExp)
//it may have attributes: hideExcl="on" - hide exclude, idMod="Exp" - add idModifier tp original id, like qorganismExp
//This is done to accomodaye comparison between standard and experimental nr
function AddOrgRow(e,orgID) {
    e = e || window.event;
    utils.preventDefault(e);
    var checkedExclude = new Array();

    var orgExclude = !jQuery("#" + orgID).attr("hideExcl") ? "ORG_EXCLUDE" : "";
    var orgIDMod = jQuery("#" + orgID).attr("idMod"); //"Exp"
    orgIDMod = (orgIDMod) ? orgIDMod : "";

    var exclName,exclID;
    if(!jQuery("#" + orgID).attr("hideExcl") ){
        exclID = "orgExcl" + orgIDMod; //orgExcl or orgExclExp
        exclName = jQuery("#" + exclID).attr("name");
    }

    var orgName = jQuery("#" + orgID).attr("name");


    var orgDict = jQuery("#" + orgID).ncbiautocomplete("option","dictionary");
    orgDict = (!orgDict || orgDict == "") ? "blast_nt_nucl_sg" : orgDict;
    var len = $(orgID).getAttribute("size");
    var crossDomainAllowed = jQuery("#" + orgID).ncbiautocomplete("option","isCrossDomain");
    var crossDomain = "";
    if(crossDomainAllowed) {
        crossDomain = ",isCrossDomain:true";
    }

    var numOrg = $("numOrg" + orgIDMod).value;
    var newOrgFieldID = orgID + numOrg;
    var newOrgField = " <div><input name=\"" + orgName + numOrg + "\" size=\"" + len + "\" id=\"" + newOrgFieldID +
                       "\" type=\"text\" data-jigconfig=\"dictionary:'" + orgDict  + "'" + crossDomain + "\" autocomplete=\"off\" data-jig=\"ncbiautocomplete\" class=\"multiOrg qorg\" />";
    var newOrgExclID;
    if (exclID) {
        var newOrgExclID = exclID + numOrg;
        newOrgField += "<div class=\"orgExcl\">" +
                       "<input type=\"checkbox\" name=\"" + exclName + numOrg + "\" class=\"oExcl cb\" id=\"" + newOrgExclID + "\" />" +
                       "<label for=\"" + newOrgExclID + "\" class=\"right oExclRl\">exclude</label></div>";
    }
    newOrgField += "</div>";
    if (navigator.userAgent.match(/ie/i)) {
        for (i = 1; i < numOrg; i++) {
            if ($(newOrgExclID)) checkedExclude[i] = $(newOrgExclID).checked;
        }
    }
    if (!navigator.userAgent.match(/firefox/i)) {
        jQuery("#orgs" + orgIDMod).append(newOrgField);
    }
    else {
        utils.insertInHtml(newOrgField, $("orgs" + orgIDMod));
    }

    if (navigator.userAgent.match(/ie/i)) {
        for (i = 1; i < numOrg; i++) {
            if ($(newOrgExclID)) $(newOrgExclID).checked = checkedExclude[i];
        }
    }
    jQuery.ui.jig.scan($(newOrgFieldID));
    setupOrganismSuggest($(newOrgFieldID));
    jQuery("#" + newOrgFieldID).ncbiautocomplete();
    if(newOrgExclID) {
        jQuery("#" + newOrgExclID).bind("click", initSingleElemPing);
    }
    $("numOrg" + orgIDMod).value++;
}

function adjustOrgVal(orgEntryElem,orgIDMod)
{
    orgIDMod = (orgIDMod) ? orgIDMod : "";
    clearOrgSuggest(orgEntryElem); //Remove suggest string
    var numOrganisms = $("numOrg" + orgIDMod).value; //1 by default    
    if ($("numOrg" + orgIDMod)) {        
        for (i = 1; i < $("numOrg" + orgIDMod).value; i++) {
            if ($("qorganism" + orgIDMod + i)) {
                clearOrgSuggest($("qorganism" + orgIDMod + i));
                if($("qorganism" + orgIDMod + i).value == "") numOrganisms--;                
            }            
        }        
    }
    $("numOrg" + orgIDMod).value = numOrganisms;
}

function validateRequiredOrganism() {
    var defaultMessage = ($("suggestHint")) ? $("suggestHint").value : "Enter organism name or id--completions will be suggested";
    var suggestHint = $("qorganism").getAttribute("suggestHint");
    if (suggestHint) defaultMessage = suggestHint;

    orgFilled = false;
    if ($("qorganism").value != "" && $("qorganism").value != defaultMessage) {
        orgFilled = true;
    }
    if (!orgFilled) {
        jQuery(".multiOrg").each(function (index) {
            if (this.value != "" && this.value != defaultMessage) {
                orgFilled = true;
            }
        });
    }
    return orgFilled;
}

function resetTopOption(event) {
    if (event.type == "ncbiautocompletechange") {
        $("qorganism").setAttribute("topOption", "");
    }
    else if (event.type == "blur") {
        var arLi = jQuery("body").find(".ui-ncbiautocomplete-options li");
        if (arLi.length > 0) {
            $("qorganism").setAttribute("topOption", arLi[0].getAttribute("acvalue"));
        }
        else {
            $("qorganism").setAttribute("topOption", "");
        }
    }
}


function validateOrganismFilter()
{
    var valid = true;

    var orgDbs = getHiddenFieldVal("ORG_DBS");
    if(orgDbs && orgDbs != undefined && orgDbs.indexOf("dbvers5") != -1) {
        valid = false;
        var hasOrganismFilter = false;
        jQuery("#filterResults").find("input[data-jig='ncbiautocomplete']").each(function (index) {
            if(jQuery(this).val() != "" && jQuery(this).val() != "Enter organism name or id--completions will be suggested") {
                hasOrganismFilter = true;
                if(index == 0) index = "";
                exclElem = jQuery("#orgExcl" + index)[0];
                if(exclElem != undefined && !exclElem.checked) {
                    valid = true;
                }
            }
        });
        if(!hasOrganismFilter) valid = true;
    }
    return valid;
}

function validateOrganismTaxid()
{
    var success = true;
    if ($("qorganism").value.indexOf("taxid") == -1) {
        var topOption = $("qorganism").getAttribute("topOption");
        if (topOption && topOption != "") {
            $("qorganism").value = topOption;
        }
    }
    if ($("qorganism").value.indexOf("taxid") == -1) {
        alert("Your organism was not found in the taxonomic lookup. Please, select a valid organism from the suggestions");
        success = false;
    }
    return success;
}

function getUrlCompForEntryField(elem) {
    var url = "";
    if (elem && elem.value != "") {
        url = "&" + elem.name + "=" + escape(elem.value);
    }
    return url;
}


function getUrlCompForCheckedField(elem) {
    var url = "";
    if (elem && elem.checked) {
        url = "&" + elem.name + "=" + elem.value;
    }
    return url;

}

function getUrlCompForOptionsField(elem) {
    var url = "";
    if (elem) {
        url = "&" + elem.name + "=" + elem[elem.selectedIndex].value;
    }
    return url;
}

function getUrlCompForMultiOptionsField(elem) {
    var url = "";
    if (elem) {
        for (i = 0; i < elem.options.length; i++) {
            if (elem.options[i].selected) {
                url += "&" + elem.name + "=" + elem.options[i].value;
            }
        }
    }
    return url;
}

function setupInputHint(inpID) {
    if (jQuery(inpID).attr("value") == "") resetInputHint(inpID);
    jQuery(inpID).bind("focus", function (e) { removeInputHint(inpID); });
}

function removeInputHint(inpID)
{
    var hint = jQuery(inpID).attr("suggesthint");
    if (hint && hint != "" && jQuery(inpID).attr("value") == hint) {
        jQuery(inpID).removeClass("orgHint");
        jQuery(inpID).attr("value","");
    }
}

function resetInputHint(inpID) {
    var hint = jQuery(inpID).attr("suggesthint");
    if (hint && hint != "") {
        jQuery(inpID).attr("value", hint);
        jQuery(inpID).addClass("orgHint");
    }
}


function calcMultiSeqNum()
{
    var seqNum = 0;
    jQuery("#dbHelpInfo").find("span.sn").each(function (index) {
        seqNum += parseInt(this.innerHTML);
    });
    if (seqNum != 0) {
        if ($("seqNum")) $("seqNum").innerHTML = "(" + seqNum + " sequences)";
    }
}

function showDbDetailsOne(dbs, params) {

    if (dbs) {

        var dbInfoUrl =  "getDBInfo.cgi";
        var rp = new RemoteDataProvider(dbInfoUrl);

        rp.onSuccess = function (obj) {
            if (g_MultipleDBS > 1) {
                if ($("dbHelpInfo").innerHTML != "") $("dbHelpInfo").innerHTML += "</br>";
                $("dbHelpInfo").innerHTML += obj.responseText;
                g_NumDbRetrieved++;
                if (g_NumDbRetrieved == g_MultipleDBS) {
                    calcMultiSeqNum();
                }
            }
            else {
                $("dbHelpInfo").innerHTML = obj.responseText;
            }
            if($("dbHelp")) $("dbHelp").setAttribute("getDbInfo", "init");
        };
        rp.onError = function(obj) {
            //alert(["error:", this.iActiveRequests, obj.status]);
            $("dbHelpInfo").innerHTML += "error, requests:" + this.iActiveRequests + " status:" + obj.status;
        }
        params = "CMD=getDbInfo&DB_PATH=" + dbs + "&" + params;

        rp.Request(params);
    }
}

function updateUserSurvey(pagetype,program,blastSpec) {

    var userSurveyUrl =  "fmtsave.cgi";
    var rp = new RemoteDataProvider(userSurveyUrl);

    rp.onSuccess = function (obj) {
        console.log("updateUserSurvey: fmtsave.cgi success, params: " + params);
    };
    rp.onError = function(obj) {
        console.log("updateUserSurvey: fmtsave.cgi error, params: " + params);
    }
    var userSurveyName = "";
    //Construct survey name <page_type>_<program>_<blast_spec>
    //For example: BlastSearch_blastp_blast2seq or BlastResults_blastn
    if(pagetype) {
        userSurveyName = pagetype;
    }
    if(program) {
        userSurveyName += (userSurveyName == "") ? program : "_" + program;
    }
    if(blastSpec) {
        userSurveyName += (userSurveyName == "") ? blastSpec : "_" + blastSpec;
    }
    var params = "CMD=Update&CUBBY_OBJECT=UserSurvey&USER_SURVEY_NAME=" + userSurveyName + "&BANNER_AD_WAS_SHOWN=true"
    rp.Request(params);
}



function initSingleElemPing()
{
    //for checkboxes:
    if (this.type == "checkbox") {
        ncbi.sg.ping(this, "click", this.checked ? "checked=true" : "checked=false");
    }
    else if (this.type == "radio") {
        ncbi.sg.ping(this, "click");
    }
    else if (this.type == "select-one") {
        //for selection boxes
        ncbi.sg.ping(this, "change", "selected=" + jQuery(this).val());
    }
}

utils.addEvent(window, 'load', newResultsWinInit, false);
utils.addEvent(window, 'load', bannerAdInit, false);


