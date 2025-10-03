const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('pages/MainPage.vue') },
      {
        path: '/games',
        component: () => import('pages/IndexPage.vue'),
      },
      { path: '/post/view/:id', component: () => import('pages/ViewPost.vue') },
      {
        path: '/games/:game',
        component: () => import('pages/CategoryPage.vue'),
      },
      { path: '/games/:game/:category', component: () => import('pages/CategoryPage.vue') },
    ],
  },

  {
    path: '/register',
    component: () => import('pages/RegistrationPage.vue'),
  },

  {
    path: '/login',
    component: () => import('pages/LoginPage.vue'),
  },

  {
    path: '/emailVerification',
    component: () => import('pages/EmailPage.vue'),
  },
  {
    path: '/сhat',
    component: () => import('layouts/ChatLayout.vue'),
    children: [
      { path: '', component: () => import('pages/ChatPage.vue') },
      {
        path: '/:user',
        component: () => import('pages/ChatPage.vue'),
      },
    ],
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    name: 'notFound',
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue'),
  },
]

export default routes
