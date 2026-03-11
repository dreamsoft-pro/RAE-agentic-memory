javascript
// Assume this is part of a larger script fetching user information.
function getUserData(userId) {
    return new Promise((resolve, reject) => {
        api.get(`/users/${userId}`).then(response => {
            resolve({
                userId: response.data.id,
                name: response.data.name,
                email: response.data.email
            });
        }).catch(error => {
            reject(`Failed to fetch user data for ${userId}: ${error.message}`);
        });
    });
}