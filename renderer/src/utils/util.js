export function is_empty(str){
    return str == null || str.length == 0;
}

export function is_url(str){
    return str.indexOf("http") == 0;
}

export function is_number(str){
    return !isNaN(str);
}

export function get_func(url, key){
    const regexfunc = [
        {
            regex: /.*\/\/x.com.*|.*twitter.com.*/g,
            funcs: [
                {
                    key: "details",
                    func: duck.twitter_get_status_details
                },{
                    key: "posts",
                    func: duck.twitter_get_user_media
                }
            ]
        },{
            regex: /.*pipix.com.*/g,
            funcs: [
                {
                    key: "details",
                    func: duck.pipixia_get_video
                }
            ]
        },{
            regex: /.*v.douyin.com.*|.*www.douyin.com.*|.*www.iesdouyin.com.*/g,
            funcs: [
                {
                    key: "details",
                    func: duck.douyin_get_video
                }
            ]
        }
    ]
    for(var i = 0; i < regexfunc.length; i++){
        if(url.match(regexfunc[i].regex)){
            for(var j = 0; j < regexfunc[i].funcs.length; j++){
                if(regexfunc[i].funcs[j].key == key){
                    return regexfunc[i].funcs[j].func;
                }
            }
        }
    }
    return null;
}