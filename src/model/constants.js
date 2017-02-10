var constants = {
	rank_bound: 100,
	messageFile: "data/message.csv",
	iconDir: "data/icon/32px/",
	iOS: {
		name: "itunes store",
		dir: "data/iOS/",
		rankFile: "ranking.csv",
		startDate: "01/01/2016",
		versionLogDir: "data/iOS/version-logs/",
		versionLogFile: ["App_Annie_Store_Stats_TimeLine_iOS_Messenger.csv",
						"App_Annie_Store_Stats_TimeLine_iOS_BIGO LIVE - Live Broadcasting.csv",
						"App_Annie_Store_Stats_TimeLine_iOS_Viber.csv",
						"App_Annie_Store_Stats_TimeLine_iOS_WeChat.csv",
						"App_Annie_Store_Stats_TimeLine_iOS_Zalo.csv"],
		},

	ggplay: {
		name: "google play store",
		dir: "data/ggplay/",
		rankFile: "ranking.csv",
		// versionLogFile: "database.csv",
		startDate: "01/01/2016",
		versionLogDir: "data/ggplay/version-logs/",
		versionLogFile: ["App_Annie_Store_Stats_TimeLine_Google Play_BIGO LIVE - Live Broadcasting.csv",
						"App_Annie_Store_Stats_TimeLine_Google Play_Messenger.csv",
						"App_Annie_Store_Stats_TimeLine_Google Play_Mocha Free SMS.csv",
						"App_Annie_Store_Stats_TimeLine_Google Play_Viber.csv",
						"App_Annie_Store_Stats_TimeLine_Google Play_WeChat.csv",
						"App_Annie_Store_Stats_TimeLine_Google Play_Zalo.csv"],
		}
}