import { createRouter, createWebHistory } from 'vue-router'
import {useUserStore} from "@/stores/user"
const modules = import.meta.glob('../views/*.vue')

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Layout',
      redirect: '/home',
      component: () => import('../layout/Layout.vue'),
      children: [
        { path: 'home', name: 'Home', component: () => import('../views/Home.vue') },
        { path: 'person', name: 'Person', component: () => import('../views/Person.vue') },
        { path: 'password', name: 'Password', component: () => import('../views/Password.vue') },
      ]
    },
    {
      path: '/login',
      name: 'Login',
      component: () => import('../views/Login.vue')
    },
	    {
      path: '/register-member',
      name: 'Register-member',
      component: () => import('../views/Register-member.vue')
    },
    {
      path: '/404',
      name: '404',
      component: () => import('../views/404.vue')
    },
	
	// Front page routing
    {
      path: '/front',
      name: 'Front',
      redirect: '/front/home',
      component: () => import('../layout/Front.vue'),
      children: [
        { path: 'home', name: 'FrontHome', component: () => import('../views/front/Home.vue') },
        { path: 'notice', name: 'notice', component: () => import('../views/front/Notice.vue') },
        { path: 'recruit', name: 'recruit', component: () => import('../views/front/Recruit.vue') },
        { path: 'lost', name: 'lost', component: () => import('../views/front/Lost.vue') },
        { path: 'cart', name: 'cart', component: () => import('../views/front/Cart.vue') },
        { path: 'orders', name: 'orders', component: () => import('../views/front/Orders.vue') },
          { path: 'notice-detail', name: 'notice-detail', component: () => import('../views/front/NoticeDetail.vue') },
          { path: 'recruit-detail', name: 'recruit-detail', component: () => import('../views/front/RecruitDetail.vue') },
          { path: 'lost-detail', name: 'lost-detail', component: () => import('../views/front/LostDetail.vue') },
      ]
    }
  ]
})

// Note: Refreshing the page will cause the page routing to reset
export const setRoutes = (menus) => {
  if (!menus || !menus.length) {
    const manager = localStorage.getItem('manager')
    if (!manager) {
      return
    }
    menus = JSON.parse(manager).managerInfo.menus
  }

  if (menus.length) {
    // Start rendering future indeterminate user-added routes
    menus.forEach(item => {   // All pages need to set routing, but directories do not need to set routing
      if (item.path) {  // Set the route if and only if path is not empty
        router.addRoute('Layout', { path: item.path, name: item.page, component: modules['../views/' + item.page + '.vue'] })
      } else {
        if (item.children && item.children.length) {
          item.children.forEach(sub => {
            if (sub.path) {
              router.addRoute('Layout', { path: sub.path, name: sub.page, component: modules['../views/' + sub.page + '.vue'] })
            }
          })
        }
      }
    })
  }
}

setRoutes()


// Route Guard
router.beforeEach((to, from, next) => {
  if (!to.matched.length) {
    next('/404')
  } else {
    next()
  }
})

export default router
