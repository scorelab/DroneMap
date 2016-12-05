module.exports = {
  development: {
    db: 'mongodb://dronemap:dronemap99@ds119728.mlab.com:19728/dronemap',
    app: {
      name: 'Nodejs Express Mongoose Demo'
    }
  },
  test: {
    db: 'mongodb://localhost/mobilitytracker',
    app: {
      name: 'Nodejs Express Mongoose Demo'
    }
  },
  production: {
    db: 'mongodb://localhost/mobilitytracker',
    app: {
      name: 'Nodejs Express Mongoose Demo'
    }
  }
};
