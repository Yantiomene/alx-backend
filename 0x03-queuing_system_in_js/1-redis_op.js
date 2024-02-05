import { createClient, print } from 'redis';

const client = createClient();

client.on('connect', () => {
  console.log('Redis client connected to the server');
}).on('error', (err) => {
  console.log(`Redis client not connected to the server: ${err}`);
});

function setNewSchool (schoolName, value) {
  client.set(schoolName, value, print);
}

function displaySchoolValue (schoolName) {
  client.get(schoolName, (error, result) => {
    if (!error) {
      console.log(result);
    }
  });
}

displaySchoolValue('Holberton');
setNewSchool('HolbertonSanFrancisco', '100');
displaySchoolValue('HolbertonSanFrancisco');
