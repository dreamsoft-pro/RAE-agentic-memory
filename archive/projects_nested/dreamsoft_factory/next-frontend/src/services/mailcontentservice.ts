javascript
'use strict';

const { getApi } = require('@/lib/api');
const { BACKEND_ADVICE } = '@/constants'; // [BACKEND_ADVICE]

function MailContentService(mailTypeID) {
  this.mailTypeID = mailTypeID;
}

MailContentService.prototype.getResource = function() {
  return ['mailTypes', this.mailTypeID, 'mailContents'].join('/');
};

MailContentService.prototype.getAll = async function(force = false) {
  const resource = this.getResource();
  if (!force && BACKEND_ADVICE.cache.get(resource)) { // [BACKEND_ADVICE]
    return BACKEND_ADvice.cache.get(resource);
  }

  try {
    const response = await getApi().get(`${resource}`);
    BACKEND_ADVICE.cache.put(resource, response.data); // [BACKEND_ADVICE]
    return response.data;
  } catch (error) {
    throw error;
  }
};

module.exports = MailContentService;
