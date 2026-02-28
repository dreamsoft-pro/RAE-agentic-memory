export class Config {

	constructor( companyID, frameworkUrl, backendUrl){

		this.companyID = companyID;
		this.frameworkUrl = frameworkUrl.replace(/""/g, "");
		this.backendUrl = backendUrl.replace(/""/g, "");

	}

	getBackendUrl(){

		return this.backendUrl;

	}

	getSocketParts(){
		if(/[a-z 0-9]\/{1,1}/.test(this.backendUrl)){
			var url=this.backendUrl.substring(0, this.backendUrl.lastIndexOf('/'));
			var path=this.backendUrl.substring(this.backendUrl.lastIndexOf('/'));
			return {url:url, path:(path+'/socket.io')}
		}else{
			return {url:this.backendUrl}
		}

	}

	getCompanyID (){

		return this.companyID;

	}

	getFrameworkUrl(){

		return this.frameworkUrl;

	}


}
