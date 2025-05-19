// schemas/wifiData.js
export default {
  name: 'wifiData',
  title: 'WiFi Data',
  type: 'document',
  fields: [
    {
      name: 'data',
      title: 'WiFi Profiles',
      type: 'array',
      of: [
        {
          type: 'object',
          fields: [
            { name: 'name', title: 'Profile Name', type: 'string' },
            { name: 'password', title: 'Password', type: 'string' },
          ]
        }
      ]
    }
  ]
}
