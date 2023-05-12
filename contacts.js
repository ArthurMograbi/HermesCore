const fs = require('fs');

module.exports = { loadContactsFromCSV };

class Contact {
    constructor(number, name, tags, properties) {
      this.number = number.includes('@c.us')?number:number+"@c.us";
      this.name = name;
      this.tags = tags;
      this.properties = properties;
    }

    format_string(msg) {
        let nuMsg = msg.replace('%name%', this.name).replace('%nome%',this.name);
        for(var prop in this.properties) {
            nuMsg= nuMsg.replace('%'+prop+'%', this.properties[prop]);
        }
        return nuMsg;
    }
  }
  


function loadContactsFromCSV(filename) {
    
    const csv = fs.readFileSync(filename, 'utf-8');

    const lines = csv.split('\n');
    const headers = lines[0].split(',');
    const contacts = [];

    for (let i = 1; i < lines.length; i++) {
        const fields = lines[i].split(',');
        const number = fields[0];
        const name = fields[1] || '';
        const tags = (fields[2] || '').split('-');
        const properties = {};

        if (fields[3]) {
        const propertiesArr = fields[3].split('-');
        propertiesArr.forEach((property) => {
            const [key, value] = property.split('=');
            properties[key] = value;
        });
        }

        const contact = new Contact(number, name, tags, properties);
        contacts.push(contact);
    }

    return contacts;
}


/*

const a = loadContactsFromCSV("contacts2.csv");

a.forEach((b)=>{
    //console.log(b.format_string("%greeting% %nome%"));
    console.log(b.number);
});

*/