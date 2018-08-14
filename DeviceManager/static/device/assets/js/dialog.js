	var dialog = {
		init: function(obj) {
			var self = this;
			self.obj = obj;
			self.buildHTML();
			self.show();
			self.bindEvt();
		},
		buildHTML: function() {
			var self = this;
			var dialogHtml;
			if (self.obj.type == 0 || !self.obj.type) {		//知道了
				dialogHtml = [
					'<div id ="' + self.obj.dialogId + '" class="err-dialog dialog">',
					'<div class="err-icon"><i class="iconfont icon-warn">&#xe623;</i></div>',
					'<div class="err-txt">' + self.obj.msg + '</div>',
					'<div class="err-btn"><a class="btn" id="J_dialog_del">知道了</a></div>',
					'</div>'
				].join('');
			} else if (self.obj.type == 1) {	//确定
				dialogHtml = self.obj.content;
			} else if (self.obj.type == 2) {	//成功
				dialogHtml = [
					'<div id ="' + self.obj.dialogId + '" class="info-dialog dialog">',
					'<div class="info-icon"><i class="iconfont icon-info">&#xe635;</i></div>',
					'<div class="info-txt">' + self.obj.msg + '</div>',
					'</div>'
				].join('');
			} else if (self.obj.type == 3) {	//确认 or 取消
				dialogHtml = [
					'<div id ="' + self.obj.dialogId + '" class="confirm-dialog dialog">',
					'<div class="confirm-icon"><i class="iconfont icon-confirm">&#xe62b;</i></div>',
					'<div class="confirm-txt">' + self.obj.msg + '</div>',
					'<div class="confirm-btn"><a class="btn dialog-btn-confirm" id="' + self.obj.confirmBtnId + '">确认</a><a class="btn dialog-btn-cancel" id="J_dialog_del">取消</a></div>',
					'<input type="hidden" value="' + self.obj.id + '">',
					'</div>'
				].join('');
			}else if (self.obj.type == 4) {		//失败
				dialogHtml = [
					'<div id ="' + self.obj.dialogId + '" class="err-unconfirm-dialog dialog">',
					'<div class="err-icon"><i class="iconfont icon-error">&#xe677;</i></div>',
					'<div class="err-txt">' + self.obj.msg + '</div>',
					'</div>'
				].join('');
			}else if (self.obj.type == 5) {		//form
				dialogHtml = [
					'<div id ="' + self.obj.dialogId + '" class="dialog-lend-device">',
					'<div class="form-header"><label class="form-label">*设备信息:</label><div class="form-group device-lend"><input type="text" class="form-control lend-content" id="device_name" name="device_name" placeholder="" value="'+ self.obj.msg +'" readonly/></div></div>',
					// '<form class="" action="/device/dc/device_list/1/" role="form" method="POST" id="lend_device"><div class="form-group" hidden><label class="form-label" for="id" hidden>*索引值:</label><div class="form-group device-lend" hidden><input type="text" class="form-control lend-content" id="id" name="id" placeholder="" value="' + self.obj.id + '" hidden></div></div><div class="form-header"><label class="form-label">*出借人:</label><div class="form-group device-lend"><input type="text" class="form-control lend-content" id="lender" name="lender" placeholder="请输入出借人名字" value=""/> </div></div></form>',
					// '<div class="confirm-btn"><a class="btn dialog-btn-confirm" id="' + self.obj.confirmBtnId + '" onclick="info_ajax(\'#lend_device\', \'/device/dc/device_list/1/\')">确认</a><a class="btn dialog-btn-cancel" id="J_dialog_del">取消</a></div>',
					'<div class="form-header"><label class="form-label">*出借人:</label><div class="form-group device-lend"><input type="text" class="form-control lend-content" id="lender" name="lender" placeholder="请输入出借人名字" value=""/> </div></div>',
					'<div class="confirm-btn"><a class="btn dialog-btn-confirm" id="' + self.obj.confirmBtnId + '">确认</a><a class="btn dialog-btn-cancel" id="J_dialog_del">取消</a></div>',
					'<input type="hidden" value="' + self.obj.id + '">',
					'</div>'
				].join('');
			}
			else if (self.obj.type == 6) {		//form
				dialogHtml = [
					'<div id ="' + self.obj.dialogId + '" class="dialog-lend-device">',
					'<div class="err-icon"><i class="iconfont icon-error">&#xe677;</i></div>',
					'<div class="err-txt">' + self.obj.msg + '</div>',
					'</div>'
				].join('');
			} else if (self.obj.type == 7) {	//成功
				dialogHtml = [
					'<div id ="' + self.obj.dialogId + '" class="dialog-lend-device">',
					'<div class="info-icon"><i class="iconfont icon-info">&#xe635;</i></div>',
					'<div class="info-txt">' + self.obj.msg + '</div>',
					'</div>'
				].join('');
			}
			dialogHtml = '<div class="dialog-mask"></div>' + dialogHtml;
			$("body").append(dialogHtml);
		},
		bindEvt: function() {
			var self = this;
			$(document).on('click', '#J_dialog_add', function() {
				self.show();
			}).on('click', '#J_dialog_del', function() {
				self.hide(self.obj.dialogId);
			});
		},
		show: function() {
			var self = this;
			$(".dialog-mask").show();
			$("#" + self.obj.dialogId).show();
		},
		hide: function() {
			var self = this;
			$(".dialog-mask").remove();
			$("#" + self.obj.dialogId).remove();
		}
	};