<template>
	<div style="height: 100%">
		<p class="title">语音情绪识别</p>
		<p class="question">{{question}}</p>
		<div class="recordBtns">
			<el-button type="primary" @click="recordStatusChange" v-if="!this.recEnd">{{recBtnText}}</el-button>
			<el-button type="primary" @click="destroyRecord" v-if="this.recorder">重置</el-button>
			<el-button type="primary" @click="endRecord" v-if="this.recorder && !this.recEnd">结束</el-button>
			<el-button type="primary" @click="playRecord" v-if="this.recEnd">播放</el-button>
			<el-button type="primary" @click="uploadProcess" v-if="this.recEnd">上传</el-button>
			<h2>录音时长：{{duration}}s</h2>
		</div>

		<el-upload :action="upload_url" :multiple="false" :file-list="fileList" :on-success="uploadSuccess" 
		:on-progress="uploadProgress" ref="upload">
			<el-button type="primary" id="upload">上传已有文件</el-button>
		</el-upload>
		
		<div v-if="processReady">
			<p class="result">初步判断：{{resultData['result']}}</p>
			<audio controls>
				<source :src="audio_url">
			</audio>
			
		</div>

		<!-- 标注数据	 -->
	</div>
</template>

<script>
import Recorder from 'js-audio-recorder'
import { baseurl, get, post } from "../network/request.js";
export default {
	data() {
		return {
			duration: '0',
			recorder: null,
			recStart: false,
			recPause: false,
			recEnd: false,
			recBtnText: '录音',
			question: '问题1：请描述一下你最近的心情，如果用一种颜色来形容的话，会是什么颜色？',
			resultData: '',
			processReady: false,
			audioMD5: '',
			audio_url: '',
			upload_url: baseurl + "uploadAudio/",
			fileList:[]
		}
	},
	methods: {
		// 是否支持录音
		canTalk() {
			return (
				window.location.protocol.indexOf('https') === 0 ||
				window.location.hostname === 'localhost' ||
				window.location.hostname === '127.0.0.1'
			)
		},
		// 开始录音
		startRecord() {
			if (!this.canTalk()) {
				this.$message({
					type: 'error',
					message:
						'由于浏览器安全策略, 非 HTTPS 或 非 localhost 访问, 录音功能不可用！',
					duration: 5000
				})
				return
			}
			if (!this.recorder) {
				this.recorder = new Recorder({
					// 以下是默认配置
					sampleBits: 16,
					sampleRate: 16000, // 浏览器默认的输入采样率,
					numChannels: 1,
				})
				this.recorder.onprocess = duration => {
					this.duration = duration.toFixed(1)
				}
				this.recorder.start().then(() => {
					console.log('开始录音')
				}).catch(err => {
					this.$alert('请插入麦克风!', '提示', {
						confirmButtonText: '确定',
						type: 'warning',
						callback: action => {
							this.recorder = null
						}
					})
					return
				})
			}
		},
		// 暂停录音
		pauseRecord() {
			this.recorder && this.recorder.pause()
			console.log('暂停录音')
		},
		// 恢复录音
		resumeRecord() {
			this.recorder && this.recorder.resume()
			console.log('恢复录音')
		},
		// 录音状态改变
		recordStatusChange() {
			if (this.recStart) {
				if (this.recPause) {		// 继续录音
					this.resumeRecord();
					this.recPause = false;
					this.recBtnText = '暂停'
				} else {			//暂停
					this.pauseRecord();
					this.recPause = true;
					this.recBtnText = '继续'
				}
			} else {				//开始
				this.startRecord();
				this.recStart = true;
				this.recBtnText = '暂停'
			}
		},
		// 结束录音
		endRecord() {
			this.recorder && this.recorder.stop();
			this.recEnd = true;
			console.log('结束录音')
		},
		// 取消录音
		destroyRecord() {
			this.recorder && this.recorder.destroy().then(() => {
				this.duration = '0'
				this.recorder = null
				this.recStart = false;
				this.recPause = false;
				this.recEnd = false;
				this.recBtnText = '录音'
				this.processReady = false;
				console.log('录音实例被销毁')
			})
		},
		// 播放录音
		playRecord() {
			this.recorder && this.recorder.play();
		},
		// 上传wav格式录音文件，此接口以后要调整到父级页面
		uploadProcess() {
			if (this.recorder) {
				this.uploadProgress()
				let blob = this.recorder.getWAVBlob();
				let formData = new FormData();
				var that = this;
				formData.append('file', blob);	//后续需要改，传多个音频

				post({
					url: baseurl + "uploadAudio/",
					data: formData
				}).then((res) => {
					// console.log(res)
					if (res.data.ok != 0) {
						that.$message({
							title: '提示',
							message: '上传完毕，音频处理中...',
							duration: 0
						});

						that.uploadSuccess(res.data);
					}
					// console.log(that.audioMD5);
				});
			}
		},

		uploadSuccess(response) {
			this.$refs.upload.clearFiles();
			var audioMD5 = response.result.data
			var that = this;

			var interval = setInterval(function () {
				get({
					url: baseurl + "getAudioResult/?audioMD5=" + audioMD5,
				}).then((res) => {
					if (res.data.ok != 0) {
						that.audio_url = baseurl + "playAudio/?audioMD5=" + audioMD5;
						that.resultData = res.data.data;
						that.processReady = true;
						clearInterval(interval);

						that.$message.closeAll();
						that.$message({
							title: '成功',
							message: '处理完成',
							type: 'success'
						});
					}
					// console.log(audioMD5);
				});
			}, 1000)
		},
		uploadProgress(){
			this.processReady = false;
		}

		/**预留接口：获取问题题目 */
		/**预留接口：上传音频文件 */
		/**预留接口：获取音频结果 */
	}
}


</script>

<style scoped>
.title {
	font-size: 32px;
	color: #fff;
	margin: 0px;
	padding-bottom: 4%;
	padding-top: 5%;
}

.question,
.result {
	font-size: 18px;
	color: #fff;
	margin: 0px;
	padding-bottom: 2%;
}

.recordBtns{
	padding-bottom: 2%;
}
</style>