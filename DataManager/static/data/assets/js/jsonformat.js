	var jsonformat = {
		init: function(obj) {
			var self = this;
			self.obj = obj;
			self.bindEvt();
		},
		isArray: function(obj) {
			return obj &&
				typeof obj === 'object' &&
				typeof obj.length === 'number' &&
				!(obj.propertyIsEnumerable('length'));
		},
		multiplyString: function(num, str) {
			var sb = [];
			for (var i = 0; i < num; i++) {
				sb.push(str);
			}
			return sb.join("");
		},
		processFormat: function(json) {
			window.TAB = this.multiplyString(2, "  ");
			var html = "";
			try {
				if (json == "") {
					json = "\"\"";
				}
				var obj = "";

				if (typeof json == 'string') {
					obj = eval("[" + json + "]");
				} else {
					obj = eval("[" + JSON.stringify(json) + "]");
				}
				html = this.processObject(obj[0], 0, false, false, false);
				$("#Canvas").html("<PRE class='CodeContainer'>" + html + "</PRE>");
			} catch (e) {
				$("#Canvas").html("<PRE class='CodeContainer1'>" + json + "</PRE>");
				// alert("JSON数据格式不正确:\n" + e.message);
			}
		},
		processObject: function(obj, indent, addComma, isArray, isPropertyContent) {
			var dateObj = new Date();
			var regexpObj = new RegExp();

			var html = "";
			var comma = (addComma) ? "<span class='Comma'>,</span> " : "";
			var type = typeof obj;
			// alert(type);
			var clpsHtml = "";
			if (this.isArray(obj)) {
				if (obj.length == 0) {
					html += this.getRow(indent, "<span class='ArrayBrace'>[ ]</span>" + comma, isPropertyContent);
				} else {
					html += this.getRow(indent, "<span class='ArrayBrace'>[</span>" + clpsHtml, isPropertyContent);
					for (var i = 0; i < obj.length; i++) {
						html += this.processObject(obj[i], indent + 1, i < (obj.length - 1), true, false);
					}
					html += this.getRow(indent, clpsHtml + "<span class='ArrayBrace'>]</span>" + comma);
				}
			} else if (type == 'object') {
				if (obj == null) {
					html += this.formatLiteral("null", "", comma, indent, isArray, "Null");
				} else if (obj.constructor == dateObj.constructor) {
					html += this.formatLiteral("new Date(" + obj.getTime() + ") /*" + obj.toLocaleString() + "*/", "", comma, indent, isArray, "Date");
				} else if (obj.constructor == regexpObj.constructor) {
					html += this.formatLiteral("new RegExp(" + obj + ")", "", comma, indent, isArray, "RegExp");
				} else {
					var numProps = 0;
					for (var prop in obj) numProps++;
					if (numProps == 0) {
						html += this.getRow(indent, "<span class='ObjectBrace'>{ }</span>" + comma, isPropertyContent);
					} else {
						html += this.getRow(indent, "<span class='ObjectBrace'>{</span>" + clpsHtml, isPropertyContent);

						var j = 0;

						for (var prop in obj) {

							var quote = "\"";

							html += this.getRow(indent + 1, "<span class='PropertyName'>" + quote + prop + quote + "</span>: " + this.processObject(obj[prop], indent + 1, ++j < numProps, false, true));

						}

						html += this.getRow(indent, clpsHtml + "<span class='ObjectBrace'>}</span>" + comma);

					}

				}

			} else if (type == 'number') {

				html += this.formatLiteral(obj, "", comma, indent, isArray, "Number");

			} else if (type == 'boolean') {

				html += this.formatLiteral(obj, "", comma, indent, isArray, "Boolean");

			} else if (type == 'function') {

				if (obj.constructor == window._regexpObj.constructor) {

					html += this.formatLiteral("new RegExp(" + obj + ")", "", comma, indent, isArray, "RegExp");

				} else {

					obj = this.formatFunction(indent, obj);

					html += this.formatLiteral(obj, "", comma, indent, isArray, "Function");

				}

			} else if (type == 'undefined') {

				html += this.formatLiteral("undefined", "", comma, indent, isArray, "Null");

			} else {

				html += this.formatLiteral(obj.toString().split("\\").join("\\\\").split('"').join('\\"'), "\"", comma, indent, isArray, "String");

			}

			return html;
		},
		formatLiteral: function(literal, quote, comma, indent, isArray, style) {
			if (typeof literal == 'string')
				literal = literal.split("<").join("&lt;").split(">").join("&gt;");
			var str = "<span class='" + style + "'>" + quote + literal + quote + comma + "</span>";
			if (isArray) str = this.getRow(indent, str);
			return str;
		},
		formatFunction: function(indent, obj) {
			var tabs = "";

			for (var i = 0; i < indent; i++) tabs += window.TAB;

			var funcStrArray = obj.toString().split("\n");

			var str = "";

			for (var i = 0; i < funcStrArray.length; i++) {

				str += ((i == 0) ? "" : tabs) + funcStrArray[i] + "\n";

			}

			return str;
		},
		getRow: function(indent, data, isPropertyContent) {
			var tabs = "";
			for (var i = 0; i < indent && !isPropertyContent; i++) tabs += window.TAB;
			if (data != null && data.length > 0 && data.charAt(data.length - 1) != "\n")
				data = data + "\n";
			return tabs + data;
		},
		bindEvt: function() {
		}
	};