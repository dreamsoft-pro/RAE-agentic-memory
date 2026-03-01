const frisby = require('frisby');
it('node-backend services', () => frisby.get('https://dreamsoft.pro:1351/getProjectsForTypes').expect('status', 200))
it('node-backend 2 services', () => frisby.get('https://printworks.pl:1351/getProjectsForTypes').expect('status', 200))
const LOCALHOST_REST = 'http://localhost:1351/rest'
it('test',  () => frisby
    .get(`${LOCALHOST_REST}/test`)
    .expect('responseTime', 500, 1000)
    .expect('status', 200)
    )
it('product', () => frisby
    .get(`${LOCALHOST_REST}/product`)
    .expect('responseTime', 500, 1000)
    .then(res => {
        console.log(res._json[0].AdminProjects[0].Formats[0].Views[0])
    }))
it('single view', () => frisby.get(`${LOCALHOST_REST}/view/59df8ccf853afe1adb1e5565`).expect('status', 200).then(res => {
    console.log(res._json)
    debugger
}))

it('ProposedTemplate', () => frisby.get(`${LOCALHOST_REST}/ProposedTemplate/59df8ccf853afe1adb1e5565`).expect('status', 200).then(res => {
    console.log(res._json)
    debugger
}))
