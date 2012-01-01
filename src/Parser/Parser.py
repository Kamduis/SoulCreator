# -*- coding: utf-8 -*-

"""
\file
\author Victor von Rhein <victor@caern.de>

\section License

Copyright (C) 2011 by Victor von Rhein

This file is part of SoulCreator.

SoulCreator is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SoulCreator is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with SoulCreator.  If not, see <http://www.gnu.org/licenses/>.
"""




from __future__ import division, print_function

from pyparsing import *




class BoolOperand(object):
	def __init__(self,t):
		self.args = t[0][0::2]


	def __str__(self):
		sep = " %s " % self.reprsymbol
		return "(" + sep.join(map(str,self.args)) + ")"




class BoolAnd(BoolOperand):
	reprsymbol = '&'


	def __nonzero__(self):
		for a in self.args:
			if isinstance(a,basestring):
				v = eval(a)
			else:
				v = bool(a)
			if not v:
				return False
		return True




class BoolOr(BoolOperand):
	reprsymbol = '|'


	def __nonzero__(self):
		for a in self.args:
			if isinstance(a,basestring):
				v = eval(a)
			else:
				v = bool(a)
			if v:
				return True
		return False




class BoolNot(BoolOperand):
	def __init__(self,t):
		self.arg = t[0][1]


	def __str__(self):
		return "~" + str(self.arg)


	def __nonzero__(self):
		if isinstance(self.arg,basestring):
			v = eval(self.arg)
		else:
			v = bool(self.arg)
		return not v




class BoolGreaterThan(BoolOperand):
	reprsymbol = '>'


	def __nonzero__(self):
		for a in self.args:
			if isinstance(a,basestring):
				v = eval(a)
			else:
				v = bool(a)
			if v:
				return True
		return False




class Parser():
	def __init__(self):
		boolOperand = Word(nums) | oneOf("True False")
		self.boolExpr = operatorPrecedence( boolOperand,
			[
			("not", 1, opAssoc.RIGHT, BoolNot),
			(">", 2, opAssoc.LEFT, BoolGreaterThan),
			("or",  2, opAssoc.LEFT,  BoolOr),
			("and", 2, opAssoc.LEFT,  BoolAnd),
			])
		#test = ["True and not False",
				#"not not True",
				#"not(True and False)",
				#"q or not p and r",
				#"q or not (p and r)",
				#"p or q or r",
				#"p or q or r and False",
				#]

		#p = True
		#q = False
		#r = True
		#print("p =", p)
		#print("q =", q)
		#print("r =", r)
		#for t in test:
			#res = boolExpr.parseString(t)[0]
			#print(t,'\n', res, '=', bool(res),'\n')


	def parse(self, string):
		result = self.boolExpr.parseString(string)
		return bool(result)




#StringBoolParser::Token StringBoolParser::nextToken() {
	#actualToken = ERROR;

	#if ( *srcPos == 0 )
		#actualToken = END;
	#else {
		#switch ( *srcPos ) {
			#case '(':
				#actualToken = LPAR;
				#break;
			#case ')':
				#actualToken = RPAR;
				#break;
		#}

		#if ( *srcPos == 'A' ) {
			#srcPos++;

			#if ( *srcPos == 'N' ) {
				#srcPos++;

				#if ( *srcPos == 'D' )
					#actualToken = AND;
				#else
					#srcPos--;
			#} else
				#srcPos--;
		#}

		#if ( *srcPos == 'O' ) {
			#srcPos++;

			#if ( *srcPos == 'R' )
				#actualToken = OR;
		#}

		#if ( *srcPos == '=' ) {
			#actualToken = EQUAL;
		#}

		#if ( *srcPos == '>' ) {
			#actualToken = GREATER;
			#srcPos++;

			#if ( *srcPos == '=' )
				#actualToken = GREATEREQUAL;
			#else
				#srcPos--;
		#}

		#if ( *srcPos == '<' ) {
			#actualToken = SMALLER;
			#srcPos++;

			#if ( *srcPos == '=' )
				#actualToken = SMALLEREQUAL;
			#else
				#srcPos--;
		#}

		#if ( *srcPos >= '0' && *srcPos <= '9' ) {
			#actualToken = NUMBER;
			#tokenNumberValue = 0;
		#}

		#while ( *srcPos >= '0' && *srcPos <= '9' ) {
			#tokenNumberValue *= 10;
			#tokenNumberValue += *srcPos - '0';
			#srcPos++;
		#}

		#if ( actualToken != NUMBER ) {
			#srcPos++;
		#}
#// 		// TEXT wird wie eine numerische 0 betrachtet.
#// 		if (( *srcPos >= 'a' && *srcPos <= 'z' ) || ( *srcPos >= 'A' && *srcPos <= 'Z' ) ) {
#// 			actualToken = TEXT;
#// 			tokenNumberValue = 0;
#// 			srcPos++;
#// 		}
#// 
#// 		while (( *srcPos >= 'a' && *srcPos <= 'z' ) || ( *srcPos >= 'A' && *srcPos <= 'Z' ) || *srcPos == '.' ) {
#// 			srcPos++;
#// 		}
#// 
#// 		if ( actualToken != TEXT ) {
#// 			srcPos++;
#// 		}
	#}

	#return actualToken;
#}

#bool StringBoolParser::compare() {
	#bool result;
	#int numberA = tokenNumberValue;

	#nextToken();

	#if ( actualToken == GREATER )    {
		#nextToken();
		#result = ( numberA > tokenNumberValue );
	#} else if ( actualToken == SMALLER )    {
		#nextToken();
		#result = ( numberA < tokenNumberValue );
	#} else if ( actualToken == GREATEREQUAL )    {
		#nextToken();
		#result = ( numberA >= tokenNumberValue );
	#} else if ( actualToken == SMALLEREQUAL )    {
		#nextToken();
		#result = ( numberA <= tokenNumberValue );
	#} else if ( actualToken == EQUAL )    {
		#nextToken();
		#result = ( numberA == tokenNumberValue );
	#} else
		#result = false;

#// 	qDebug() << Q_FUNC_INFO << result;

	#return result;
#}


#bool StringBoolParser::paranthesis() {
	#bool result;

#// 	qDebug() << Q_FUNC_INFO << actualToken << ",";

	#switch ( actualToken ) {
		#case NUMBER:
		#case TEXT:
			#result = compare();
			#return result;

		#case LPAR:
			#nextToken();
			#result = operatorAND();

			#if ( actualToken != RPAR )
				#return true;

			#return result;

		#case END:
			#return false;
	#}

	#throw Exception( "primary expected" );
#}

#bool StringBoolParser::operatorOR() {
	#bool result;

	#result = paranthesis();

	#nextToken();

#// 	qDebug() << Q_FUNC_INFO << actualToken << ",";

	#while ( actualToken == OR ) {
		#nextToken();
		#result = operatorAND() || result;
	#}

#// 	qDebug() << Q_FUNC_INFO << result;

	#return result;
#}

#bool StringBoolParser::operatorAND() {
	#bool result;

	#result = operatorOR();

	#while ( actualToken == AND ) {
		#nextToken();

#// 		qDebug() << Q_FUNC_INFO << actualToken << ",";

		#result = operatorAND() && result;
	#}

#// 	qDebug() << Q_FUNC_INFO << result;

	#return result;
#}

#bool StringBoolParser::validate( QString checkString ) {
	#checkString.remove( QRegExp( "\\s" ) );
	#QByteArray saveAsBytes = checkString.toAscii();
	#char *ptr = saveAsBytes.data();

	#srcPos = ptr;
	#nextToken();
	#return operatorAND();
#}
