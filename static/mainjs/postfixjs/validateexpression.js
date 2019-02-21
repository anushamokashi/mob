
var DEBUG_ON = false;


var lstAlpha = "a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,uv,w,x,y,z";
var lstDigits = "0,1,2,3,4,5,6,7,8,9";
var lstArithOps = "^,*,/,%,+,-";
var lstLogicOps = "!,&,|";
var lstCompaOps = "<,<=,>,>=,<>,=";
var lstFuncOps = ["ABS", "DATE", "UCASE", "LCASE", "LOWER", "TIME", "ROUND",
		"STR", "EVAL", "AMTWORD", "CURRAMTWORD", "RND", "POWER", "SUBSTR",
		"REVERSESTRING", "GETLENGTH", "PAD", "LEFTPAD", "GETMOD", "TRIMVAL",
		"TRIM", "VAL", "STUFF", "IIF", "ISEMPTYVALUE", "FINDANDREPLACE",
		"FORMATVALUE", "FORMATAMOUNT", "FORMATACCAMOUNT", "INSTR", "ADDTODATE",
		"ADDTOMONTH", "YEAROFDATE", "LASTDAYOFMONTH", "MONTHOFDATE",
		"CMONTHYEAR", "MAKEDATE", "MANDY", "YANDM", "DTOC", "CTOD","WEEKNO",
		"DAYSELAPSED", "DAYOFDATE", "TIMEELAPSED", "ADDTOTIME", "ISEMPTYVALUE",
		"ISEMPTY", "GETINTEGER", "UPPER", "VALIDENCODEDATE", "TOTAL", "GETMIN",
		"GETMAX", "GETROWCOUNT", "GETVALUE", "GETROW", "SUM", "SUMTILL",
		"SETVALUE", "REFRESHFIELD","FORCEREFRESHFIELD","VIEWTRANSACTION","OPENURL","ADDCONTEXTMENU","VIEWREPORT","ADDICON", "FORMATDATETIME", "CELL", "GETSUBTOTAL",
		"GETID", "GETOLD", "SQLREGVAR", "REGVAR", "SETPROPERTY", "FIRESQL",
		"SQLGET", "GEN_ID", "FINDRECORD", "HIDEFRAME", "REFRESHFRAME","LOADDATA","GRIDCOLCONCAT",
		"INITGRID", "ACTIVATEFIELD", "ENABLEBUTTON", "ALLOWFRAMECHANGE",
		"SETSYSTEMVAR", "RESETACTIVECOMP","OPENTRANSFORM","EXECUTEOPTION","FIELDCHANGED","FIELDCHANGEDBOOLEAN","SETSEQUENCE","GETROUNDOFF",
		"GETCOSTRATEWOLOC","GETCOSTRATEWLOC","GETCLOSINGSTOCKWOLOC","GETCLOSINGSTOCKWLOC","CHECKSTOCKWOLOC","CHECKSTOCKWLOC",
		"GETSTOCKAGE","GETSTOCKVALUEWLOC","GETSTOCKVALUEWOLOC","HIDECOLUMN","UNHIDECOLUMN","ADDOPTION","REFRESHVIEW","FORCEVOUCHERADJUSTMENTBEFORESAVE","EDITCOLUMN","SETCOLUMNVALUE",
		"SETCELLFONT","ISVALIDDROP","CEIL","POSTRECORD","GETCELL","SETDECIMALTONUMBER","APPENDNUMBER","DIRECTPRINTFORMAT","GETRCELL","DRAWHTMLTABLE",
		"FIRESQLARRAY","PRINTPREVIEW","SEARCHUTILITY","CURRENTDAYOFWEEK","HIDECOLUMNREPORT","SENDSMS","SENDMAIL",
		"DATETIME","STRLENGTH","BCSSERVERDATE","BCSSERVERTIME","REMAININGDAYSOFMONTH",
		"GETDAYSINMONTH","SETTOTALVALUE","MULTIPRINTPREVIEW","MENUITEM","REMAINDER"
		,"FILEARCHIVEBEFORESAVE","FILEARCHIVEEXISTS","SETPREVIEWSTATUS","SETFILLGRIDNAME","CONTAINS","SHOWALERT","FIRESQLCACHEFORNONGRID","FIRESQLCACHEFORGRID","CLOSEEFORM","CACHESQLGET","GETFIRSTDATEOFMONTH","TRANSPOSETOEFORM","GETSQLLIST","OPENEREPORT","SHOWDIALOG","EFORMPOPUP","LINKFORMTRANS","GETHOURS","OPENPAGE","GETAGE","GETDAYS","GETAGEANDDAYS","FLOOR","TRUNC"];
		  

var th = ['', 'thousand', 'million', 'billion', 'trillion'];
var dg = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven',
		'eight', 'nine'];
var tn = ['ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen',
		'sixteen', 'seventeen', 'eighteen', 'nineteen'];
var tw = ['twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty',
		'ninety'];
var UNARY_NEG = "?";
var ARG_TERMINAL = "?%";
var DEBUG_ON = false;





/*------------------------------------------------------------------------------
 * NAME       : IsNumber
 * PURPOSE    : Checks whether the specified parameter is a number.
 * RETURNS    : True - If supplied parameter can be succesfully converted to a number
 *              False - Otherwise
 *----------------------------------------------------------------------------*/
function IsNumber(pstrVal) {
	var dblNo = Number.NaN;
    
	if(pstrVal === " "){
	      dblNo = Number.NaN;
	}else{
	dblNo = new Number(pstrVal);
	}
	if (isNaN(dblNo))
	{
		return false;
	}
	return true;
}

/*------------------------------------------------------------------------------
 * NAME       : IsBoolean
 * PURPOSE    : Checks whether the specified parameter is a boolean value.
 * PARAMETERS : pstrVal - The string to be checked.
 * RETURNS    : True - If supplied parameter is a boolean constant
 *              False - Otherwise
 *----------------------------------------------------------------------------*/
function IsBoolean(pstrVal) {
	var varType = typeof(pstrVal);
	var strTmp = null;

	if (varType == "boolean")
	{
		return true;
	}
	if (varType == "number" || varType == "function" || varType == undefined)
	{
		return false;
	}
	if (IsNumber(pstrVal))
	{
		return false;
	}
	if (varType == "object") {
		strTmp = pstrVal.toString();
		if (strTmp.toUpperCase() == "TRUE" || strTmp.toUpperCase() == "FALSE")
		{
			return true;
		}
	}
	if (pstrVal == null || typeof(pstrVal) != 'string') {

		return true;

	}
	if (pstrVal.toUpperCase() == "TRUE" || pstrVal.toUpperCase() == "FALSE")
	{
		return true;
	}
	return false;
}

/*------------------------------------------------------------------------------
 * NAME       : ToNumber
 * PURPOSE    : Converts the supplied parameter to numaric type.
 * PARAMETERS : pobjVal - The string to be converted to equvalent number.
 * RETURNS    : numeric value if string represents a number
 * THROWS     : Exception if string can not be converted 
 *----------------------------------------------------------------------------*/
function ToNumber(pobjVal) {
	var dblRet = Number.NaN;

	if (typeof(pobjVal) == "number")
	{
		return pobjVal;
	}
	else {
		dblRet = new Number(pobjVal);
		if (isNaN(dblRet.valueOf()))
		{
			return pobjVal;
		}
		else
		{
			return dblRet.valueOf();
		}
	}
}

/*------------------------------------------------------------------------------
 * NAME       : ToBoolean
 * PURPOSE    : Converts the supplied parameter to boolean value
 * PARAMETERS : pobjVal - The parameter to be converted.
 * RETURNS    : Boolean value
 *----------------------------------------------------------------------------*/
function ToBoolean(pobjVal) {
	var dblNo = Number.NaN;
	var strTmp = null;

	if (pobjVal == null || pobjVal == undefined)
	{
		throw "Boolean value is not defined!";
	}
	else if (typeof(pobjVal) == "boolean")
	{
		return pobjVal;
	}
	else if (typeof(pobjVal) == "number")
	{
		return (pobjval > 0);
	}
	else if (IsNumber(pobjVal)) {
		dblNo = ToNumber(pobjVal);
		if (isNaN(dblNo))
		{
			return null;
		}
		else
		{
			return (dblNo > 0);
		}
	} else if (typeof(pobjVal) == "object") {
		strTmp = pobjVal.toString();
		if (strTmp.toUpperCase() == "TRUE")
		{
			return true;
		}
		else if (strTmp.toUpperCase() == "FALSE")
		{
			return false;
		}
		else
		{
			return null;
		}
	} else if (typeof(pobjVal) == "string") {
		if (pobjVal.toUpperCase() == "TRUE")
		{
			return true;
		}
		else if (pobjVal.toUpperCase() == "FALSE")
		{
			return false;
		}
		else
		{
			return null;
		}
	} else
	{
		return null;
	}
}
/*------------------------------------------------------------------------------
 * NAME       : isFloat
 * PURPOSE    : To check whether the given number is Float or Not
 * PARAMETERS : num-Number
 * RETURNS    : Boolean
 *----------------------------------------------------------------------------*/
function isFloat(num) {
	if (IsNumber(num)) {
		var str = num.toString();

		if (str.indexOf('.') != -1) {
			return true;
		} else {
			return false;
		}
	}
	return false;
}

/*------------------------------------------------------------------------------
 * NAME       : isInt
 * PURPOSE    : To check whether the given number is integer or Not
 * PARAMETERS : num-Number
 * RETURNS    : Boolean
 *----------------------------------------------------------------------------*/
function isInt(num) {
	if (IsNumber(num)) {
		var str = num.toString();

		if (str.indexOf('.') == -1) {
			return true;
		} else {
			return false;
		}
	}
	return false;
}

/*------------------------------------------------------------------------------
 * NAME       : RTrim
 * PURPOSE    : Removes trailing spaces from a string.
 * PARAMETERS : pstrValue - The string from which trailing spaces are to be removed.
 * RETURNS    : A string with trailing spaces removed.
 *----------------------------------------------------------------------------*/
function RTrim(pstrValue) {

	if(pstrValue != null || pstrValue != undefined){
	var w_space = String.fromCharCode(32);
	var v_length = pstrValue.length;
	var strTemp = "";
	if (v_length < 0) {
		return "";
	}
	var iTemp = v_length - 1;

	while (iTemp > -1) {
		if (pstrValue.charAt(iTemp) == w_space) {
		} else {
			strTemp = pstrValue.substring(0, iTemp + 1);
			break;
		}
		iTemp = iTemp - 1;
	}
	return strTemp;
	}
}


/*------------------------------------------------------------------------------
 * NAME       : IsOperator
 * PURPOSE    : Checks whether the string specified by strArg is an operator
 * PARAMETERS : strArg - The string to be checked
 * RETURNS    : False - If strArg is not an operator symbol
 *              True - Otherwise 
 *----------------------------------------------------------------------------*/
function IsOperator(strArg) {
	if (lstArithOps.indexOf(strArg) >= 0 || lstCompaOps.indexOf(strArg) >= 0)
	{
		return true;
	}
	return false;
}

/*------------------------------------------------------------------------------
 * NAME       : LTrim
 * PURPOSE    : Removes leading spaces from a string.
 * PARAMETERS : pstrValue - The string from which leading spaces are to be removed.
 * RETURNS    : A string with leading spaces removed.
 *----------------------------------------------------------------------------*/
function LTrim(pstrValue) {

	if(pstrValue != null || pstrValue != undefined){
	var w_space = String.fromCharCode(32);
	if (v_length < 1) {
		return "";
	}
	var v_length = pstrValue.length;
	var strTemp = "";
	var iTemp = 0;

	while (iTemp < v_length) {
		if (pstrValue.charAt(iTemp) == w_space) {
		} else {
			strTemp = pstrValue.substring(iTemp, v_length);
			break;
		}
		iTemp = iTemp + 1;
	}
	return strTemp;
	}
}


/*------------------------------------------------------------------------------
 * NAME       : Trim
 * PURPOSE    : Removes trailing and leading spaces from a string.
 * PARAMETERS : pstrVal - The string from which leading and trailing spaces are 
 *              to be removed.
 * RETURNS    : A string with leading and trailing spaces removed.
 *----------------------------------------------------------------------------*/
function Trim(pstrVal) {
	
   if(typeof pstrVal ==  "string" ){
	if(pstrVal.substr(0,2)=='{}'){
		return pstrVal;
	}
   }
   
	if(typeof pstrVal == "number")
	{
		return pstrVal;
	}
	
	if(pstrVal !=null || pstrVal != undefined){
	if (pstrVal.length < 1)
	{
		return "";
	}

	pstrVal = RTrim(pstrVal);
	pstrVal = LTrim(pstrVal);
	if (pstrVal == "")
	{
		return "";
	}
	else
	{
		return pstrVal;
	}
  }      

}

/*------------------------------------------------------------------------------
 * NAME       : Tokanize
 * PURPOSE    : Breaks the string into a token array. It also checks whether the
 *              parenthesis, single quotes and double quotes are balanced or not.
 * PARAMETERS : inputExpression - The string from which token array is to be 
 *              constructed.
 * RETURNS    : An array of tokens.
 * THROWS     : Unterminated string constant - Single/Double quotes are not 
 *                                             properly terminated
 *              Unbalanced parenthesis - Opening/closing braces are not balanced
 *----------------------------------------------------------------------------*/
function Tokanize(inputExpression)// Here V pass the Expression To be
									// Evaluated
{
	var intCntr, intBraces;
	var arrTokens;
	var intIndex, intPos;
	var chrChar, chrNext;
	var strToken, prevToken;

	intCntr = 0;
	intBraces = 0;
	intIndex = 0;
	strToken = "";
	arrTokens = new Array();
	pstrExpression = Trim(inputExpression);
	while (intCntr < pstrExpression.length) {
		prevToken = "";
		chrChar = pstrExpression.substr(intCntr, 1);
		/*
		 * if (window) if (window.status) window.status = "Processing " +
		 * chrChar;
		 */
		switch (chrChar) {
			case " " :
				if (strToken.length > 0) {
					arrTokens[intIndex] = strToken;
					intIndex++;
					strToken = "";
				}
				break;
			case "(" :
				intBraces++;
				if (strToken.length > 0) {
					arrTokens[intIndex] = strToken;
					intIndex++;
					strToken = "";
				}
				arrTokens[intIndex] = chrChar;
				intIndex++;
				break;
			case ")" :
				intBraces--;
				if (strToken.length > 0) {
					arrTokens[intIndex] = strToken;
					intIndex++;
					strToken = "";
				}
				arrTokens[intIndex] = chrChar;
				intIndex++;
				break;
			case "^" :
				if (strToken.length > 0) {
					arrTokens[intIndex] = strToken;
					intIndex++;
					strToken = "";
				}
				arrTokens[intIndex] = chrChar;
				intIndex++;
				break;
			case "*" :
				if (strToken.length > 0) {
					arrTokens[intIndex] = strToken;
					intIndex++;
					strToken = "";
				}
				arrTokens[intIndex] = chrChar;
				intIndex++;
				break;
			case "/" :
				if (strToken.length > 0) {
					arrTokens[intIndex] = strToken;
					intIndex++;
					strToken = "";
				}
				arrTokens[intIndex] = chrChar;
				intIndex++;
				break;
			case "%" :
				if (strToken.length > 0) {
					arrTokens[intIndex] = strToken;
					intIndex++;
					strToken = "";
				}
				arrTokens[intIndex] = chrChar;
				intIndex++;
				break;
			case "&" :
				if (strToken.length > 0) {
					arrTokens[intIndex] = strToken;
					intIndex++;
					strToken = "";
				}
				arrTokens[intIndex] = chrChar;
				intIndex++;
				break;
			case "|" :
				if (strToken.length > 0) {
					arrTokens[intIndex] = strToken;
					intIndex++;
					strToken = "";
				}
				arrTokens[intIndex] = chrChar;
				intIndex++;
				break;
			case "," :
				if (strToken.length > 0) {
					arrTokens[intIndex] = strToken;
					intIndex++;
					strToken = "";
				}
				arrTokens[intIndex] = chrChar;
				intIndex++;
				break;
			case "-" :
				if (strToken.length > 0) {
					arrTokens[intIndex] = strToken;
					intIndex++;
					strToken = "";
				}
				chrNext = pstrExpression.substr(intCntr + 1, 1);
				if (arrTokens.length > 0)
			    {
					prevToken = arrTokens[intIndex - 1];
				}
				if (intCntr == 0
						|| ((IsOperator(prevToken) || prevToken == "(" || prevToken == ",") && (IsDigit(chrNext) || chrNext == "("))) {
					// Negative Number
					strToken += chrChar;
				} else {
					arrTokens[intIndex] = chrChar;
					intIndex++;
					strToken = "";
				}
				break;
			case "+" :
				if (strToken.length > 0) {
					arrTokens[intIndex] = strToken;
					intIndex++;
					strToken = "";
				}
				chrNext = pstrExpression.substr(intCntr + 1, 1);
				if (arrTokens.length > 0)
			    {
					prevToken = arrTokens[intIndex - 1];
				}
				if (intCntr == 0
						|| ((IsOperator(prevToken) || prevToken == "(" || prevToken == ",") && (IsDigit(chrNext) || chrNext == "("))) {
					// positive Number
					strToken += chrChar;
				} else {
					arrTokens[intIndex] = chrChar;
					intIndex++;
					strToken = "";
				}
				break;
			case "<" :
				chrNext = pstrExpression.substr(intCntr + 1, 1);
				if (strToken.length > 0) {
					arrTokens[intIndex] = strToken;
					intIndex++;
					strToken = "";
				}
				if (chrNext == "=") {
					arrTokens[intIndex] = chrChar + "=";
					intIndex++;
					intCntr++;
				} else if (chrNext == ">") {
					arrTokens[intIndex] = chrChar + ">";
					intIndex++;
					intCntr++;
				} else {
					arrTokens[intIndex] = chrChar;
					intIndex++;
				}
				break;
			case ">" :
				chrNext = pstrExpression.substr(intCntr + 1, 1);
				if (strToken.length > 0) {
					arrTokens[intIndex] = strToken;
					intIndex++;
					strToken = "";
				}
				if (chrNext == "=") {
					arrTokens[intIndex] = chrChar + "=";
					intIndex++;
					intCntr++;
				} else {
					arrTokens[intIndex] = chrChar;
					intIndex++;
				}
				break;
			case "=" :
				if (strToken.length > 0) {
					arrTokens[intIndex] = strToken;
					intIndex++;
					strToken = "";
				}
				arrTokens[intIndex] = chrChar;
				intIndex++;
				break;
			case "'" :
				if (strToken.length > 0) {
					arrTokens[intIndex] = strToken;
					intIndex++;
					strToken = "";
				}

				intPos = pstrExpression.indexOf(chrChar, intCntr + 1);
				if (intPos < 0){
					
		            return ["error","uncaught exception:Unterminated string constant"] ;
				}
				else {
					strToken += pstrExpression.substring(intCntr + 1, intPos);
					arrTokens[intIndex] = strToken;
					intIndex++;
					strToken = "";
					intCntr = intPos;
				}
				break;
			case "{" :

				if (strToken.length > 0) {

					arrTokens[intIndex] = "{}" + strToken;
					intIndex++;
					strToken = "";
				}

				intPos = pstrExpression.indexOf("}", intCntr + 1);	
				
  
				if (intPos < 0) {
					
		           
		            
		            return ["error","uncaught exception:Unterminated string constant!"];
				}
				else{
					strToken += pstrExpression.substring(intCntr + 1, intPos);						
					strToken=strToken.replace("{","{}");
					var matchedPattern = strToken.match(/{}/g);
					if(matchedPattern!=null){
                    var i=1;
					strToken="";
					while(i<=matchedPattern.length){					                         						 
						 intPos = pstrExpression.indexOf("}", intPos+1);
						 i++;
						 }
				    strToken += pstrExpression.substring(intCntr + 1, intPos);
					}				    
					strToken=strToken.replace("{}","{");
					arrTokens[intIndex] = "{}" + strToken;
					intIndex++;
					strToken = "";
					intCntr = intPos;
				}

				break;
			default :
				strToken += chrChar;
				break;
		}
		intCntr++;
	}
	if (intBraces > 0){

		return ["error","This expression have Unbalanced parenthesis!"];
	}

	if (strToken.length > 0)
	{
		arrTokens[intIndex] = strToken;
	}
	
    //var InFixToPostFixExpr = ;
	//var InFixToPostFixExprObj = {"success",InFixToPostFix(arrTokens).toString() };
	
	return ["success",InFixToPostFix(arrTokens).toString()];
}


/*------------------------------------------------------------------------------
 * NAME       : Precedence
 * PURPOSE    : Returns the precedence of a given operator
 * PARAMETERS : pstrTok - The operator token whose precedence is to be returned.
 * RETURNS    : Integer
 *----------------------------------------------------------------------------*/
function Precedence(pstrTok) {
	var intRet = 0;

	switch (pstrTok) {
		case "+" :
		case "-" :
			intRet = 5;
			break;
		case "*" :
		case "/" :
		case "%" :
			intRet = 6;
			break;
		case "^" :
			intRet = 7;
			break;
		case UNARY_NEG :
		case "!" :
			intRet = 10;
			break;
		case "(" :
			intRet = 99;
			break;
		case "&" :
		case "|" :
			intRet = 3;
			break;
		case ">" :
		case ">=" :
		case "<" :
		case "<=" :
		case "=" :
		case "<>" :
			intRet = 4;
			break;
		default :
			if (IsFunction(pstrTok))
		{
			intRet = 9;
		}
			else
		    {
				intRet = 0;
			}
			break;
	}
	debugAssert("Precedence of " + pstrTok + " is " + intRet);
	return intRet;
}


// Returns size of stack
function getSize() {
	return this.intIndex;
}

/*------------------------------------------------------------------------------
 * NAME       : IsFunction
 * PURPOSE    : Checks whether the string specified by strArg is a function name
 * PARAMETERS : strArg - The string to be checked
 * RETURNS    : False - If strArg is not a valid built-in function name.
 *              True - Otherwise 
 *----------------------------------------------------------------------------*/
function IsFunction(strArg) {
	var idx = 0;

	strArg = strArg.toUpperCase();
	for (idx = 0; idx < lstFuncOps.length; idx++) {
		if (strArg == lstFuncOps[idx])
		{
			return true;
		}
	}
	return false;
}




// This method pushes a new element onto the top of the stack
function pushElement(newData) {
	// Assign our new element to the top
	debugAssert("Pushing " + newData);
	this.arrStack[this.intIndex] = newData;
	this.intIndex++;
}

// This method pops the top element off of the stack
function popElement() {
	var retVal;

	retVal = null;
	if (this.intIndex > 0) {
		// Assign our new element to the top
		this.intIndex--;
		retVal = this.arrStack[this.intIndex];
	}
	return retVal;
}

// Gets an element at a particular offset from top of the stack
function getElement(intPos) {
	var retVal;

	// alert ("Size : " + this.intIndex + ", Index " + intPos);
	if (intPos >= 0 && intPos < this.intIndex)
	{
		retVal = this.arrStack[this.intIndex - intPos - 1];
	}
	return retVal;
}


// Converts stack contents into a comma seperated string
function dumpStack() {
	var intCntr = 0;
	var strRet = "";
	if (this.intIndex == 0)
	{
		return null;
	}
	for (intCntr = 0; intCntr < this.intIndex; intCntr++) {
		if (strRet.length == 0)
		{
			strRet += this.arrStack[intCntr];
		}
		else
		{
			strRet += "," + this.arrStack[intCntr];
		}
	}
	return strRet;
}

/*------------------------------------------------------------------------------
 * NAME       : debugAssert
 * PURPOSE    : Shows a messagebox displaying supplied message
 * PARAMETERS : pObject - The object whose string representation is to be displayed.
 * RETURNS    : Nothing
 *----------------------------------------------------------------------------*/
function debugAssert(pObject) {
	if (DEBUG_ON)
	{
		//alert(pObject.toString());
	}
}



// This method tells us if this Stack object is empty
function isStackEmpty() {
	if (this.intIndex == 0)
	{
		return true;
	}
	else
	{
		return false;
	}
}

/*******************************************************************************
 * BCS_Stack.js
 ******************************************************************************/

function Stack() {
	this.arrStack = new Array();
	this.intIndex = 0;

	this.Size = getSize;
	this.IsEmpty = isStackEmpty;
	this.Push = pushElement;
	this.Pop = popElement;
	this.Get = getElement;
	this.toString = dumpStack;
}

	/*------------------------------------------------------------------------------
	 * NAME       : InFixToPostFix
	 * PURPOSE    : Convert an Infix expression into a postfix (RPN) equivalent
	 * PARAMETERS : Infix expression element array
	 * RETURNS    : array containing postfix expression element tokens
	 *----------------------------------------------------------------------------*/
	function InFixToPostFix(arrToks) {
		var myStack;
		var intCntr, intIndex;
		var strTok, strTop, strNext, strPrev;
		var blnStart;

		blnStart = false;
		intIndex = 0;
		arrPFix = new Array();
		myStack = new Stack();

		// Infix to postfix converter
		for (intCntr = 0; intCntr < arrToks.length; intCntr++) {
			strTok = arrToks[intCntr];
			debugAssert("Processing token [" + strTok + "]");
			switch (strTok) {
				case "(" :
					if (myStack.Size() > 0 && IsFunction(myStack.Get(0))) {
						arrPFix[intIndex] = ARG_TERMINAL;
						intIndex++;
					}
					myStack.Push(strTok);
					break;
				case ")" :
					blnStart = true;
					debugAssert("Stack.Pop [" + myStack.toString());
					while (!myStack.IsEmpty()) {
						strTok = myStack.Pop();
						if (strTok != "(") {
							arrPFix[intIndex] = strTok;
							intIndex++;
						} else {
							blnStart = false;
							break;
						}
					}
					if (myStack.IsEmpty() && blnStart){
					
					console.log("This expression Unbalanced parenthesis!");
					break;
					}
						
					break;
				case "," :
					if (myStack.IsEmpty())
						{
						break;
						}
					debugAssert("Pop stack till opening bracket found!");
					while (!myStack.IsEmpty()) {
						strTok = myStack.Get(0);
						if (strTok == "(")
							{
							break;
							}
						arrPFix[intIndex] = myStack.Pop();
						intIndex++;
					}
					break;
				case "!" :
				case "-" :
					// check for unary negative operator.
					if (strTok == "-") {
						strPrev = null;
						if (intCntr > 0)
							{
							strPrev = arrToks[intCntr - 1];
							}
						strNext = arrToks[intCntr + 1];
						if (strPrev == null || IsOperator(strPrev)
								|| strPrev == "(") {
							debugAssert("Unary negation!");
							strTok = UNARY_NEG;
						}
					}
				case "^" :
				case "*" :
				case "/" :
				case "%" :
				case "+" :
					// check for unary + addition operator, we need to ignore
					// this.
					if (strTok == "+") {
						strPrev = null;
						if (intCntr > 0)
							{
							strPrev = arrToks[intCntr - 1];
							}
						strNext = arrToks[intCntr + 1];
						if (strPrev == null || IsOperator(strPrev)
								|| strPrev == "(") {
							debugAssert("Unary add, Skipping");
							break;
						}
					}
				case "&" :
				case "|" :
				case ">" :
				case "<" :
				case "=" :
				case ">=" :
				case "<=" :
				case "<>" :
					strTop = "";
					if (!myStack.IsEmpty())
						{
						strTop = myStack.Get(0);
						}
					if (myStack.IsEmpty()
							|| (!myStack.IsEmpty() && strTop == "(")) {
						debugAssert("Empty stack pushing operator [" + strTok
								+ "]");
						myStack.Push(strTok);
					} else if (Precedence(strTok) > Precedence(strTop)) {
						debugAssert("[" + strTok
								+ "] has higher precedence over [" + strTop
								+ "]");
						myStack.Push(strTok);
					} else {
						// Pop operators with precedence >= operator strTok
						while (!myStack.IsEmpty()) {
							strTop = myStack.Get(0);
							if (strTop == "("
									|| Precedence(strTop) < Precedence(strTok)) {
								debugAssert("[" + strTop
										+ "] has lesser precedence over ["
										+ strTok + "]");
								break;
							} else {
								arrPFix[intIndex] = myStack.Pop();
								intIndex++;
							}
						}
						myStack.Push(strTok);
					}
					break;
				default :
					if (!IsFunction(strTok)) {
						debugAssert("Token [" + strTok
								+ "] is a variable/number!");
						// Token is an operand
						if (IsNumber(strTok))
							{
							strTok;
							}
						// strTok = ToNumber(strTok);
						else if (IsBoolean(strTok))
							{
							strTok = ToBoolean(strTok);
							}
						/*
						 * else if (isDate(strTok, dtFormat)) strTok =
						 * getDateFromFormat(strTok, dtFormat);
						 */
						arrPFix[intIndex] = strTok;
						intIndex++;
						break;
					} else {
						strTop = "";
						if (!myStack.IsEmpty())
							{
							strTop = myStack.Get(0);
							}
						if (myStack.IsEmpty()
								|| (!myStack.IsEmpty() && strTop == "(")) {
							debugAssert("Empty stack pushing operator ["
									+ strTok + "]");
							myStack.Push(strTok);
						} else if (Precedence(strTok) > Precedence(strTop)) {
							debugAssert("[" + strTok
									+ "] has higher precedence over [" + strTop
									+ "]");
							myStack.Push(strTok);
						} else {
							// Pop operators with precedence >= operator in
							// strTok
							while (!myStack.IsEmpty()) {
								strTop = myStack.Get(0);
								if (strTop == "("
										|| Precedence(strTop) < Precedence(strTok)) {
									debugAssert("[" + strTop
											+ "] has lesser precedence over ["
											+ strTok + "]");
									break;
								} else {
									arrPFix[intIndex] = myStack.Pop();
									intIndex++;
								}
							}
							myStack.Push(strTok);
						}
					}
					break;
			}
			debugAssert("Stack   : " + myStack.toString() + "\n" + "RPN Exp : "
					+ arrPFix.toString());

		}

		// Pop remaining operators from stack.
		while (!myStack.IsEmpty()) {
			arrPFix[intIndex] = myStack.Pop();
			intIndex++;
		}
		return arrPFix;
	}
