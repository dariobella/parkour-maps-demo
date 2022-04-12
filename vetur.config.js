module.exports = {
  settings: {
    "vetur.useWorkspaceDependencies": true,
    "vetur.experimental.templateInterpolationService": true
  },
  projects: [
    './frontend/',
    {
      root: './frontend/',
      globalComponents: [
        '.frontend/src/components/*.vue'
      ]
    }
  ]
}