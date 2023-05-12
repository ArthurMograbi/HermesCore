// Monitor new message
// Read new messages
// Return stats, keyword ocurrences




class Monitor{
    constructor(auto_actions, verbose){
        this.aa=auto_actions||[];
        if(verbose) this.aa.push(console.log);
        this.msgs={};
        this.props = {};
    }

    async receiveMsg(msg){
        this.msgs[msg.from]=msg.from in this.msgs?this.msgs[msg.from].concat([msg.body]):[msg.body];
        this.aa.forEach((fun) => {
            fun(msg);
        });
    }

    allMsgs(){
        const allmsg = [];
        for(var user in this.msgs) {
            this.msgs[user].forEach((msg)=>{
                allmsg.push(msg);
            });
        }
        return allmsg;
    }
}

module.exports = { Monitor };


const ff = (msg)=>{console.log(msg.body)};
/*
const a = new Monitor([],true);
a.aa.push(ff);
console.log(a.receiveMsg({from:'31331313',body:"Hello"}));
console.log(a.receiveMsg({from:'31331313',body:"How are you?"}));
console.log(a.receiveMsg({from:'22222313',body:"Bleh"}));
console.log(a.allMsgs());

*/