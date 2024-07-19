import { createRouter,createWebHashHistory } from "vue-router";
import Home from "../views/Home.vue";

const routes = [
    {
        path:'/home',
        name:'home',
        component:Home,
        redirect: '/index',
        children: [
            {
                path:'/index',
                name:'index',
                component: () => import('@/views/Index/index.vue'),
                meta:{
                    title:'首页',
                    menu: true,
                    keepAlive: true
                },
            },
            {
                path:'/video',
                name:'video',
                component: () => import('@/views/Video/index.vue'),
                // children: [
                //     {
                //         path:'/video/twitter',
                //         name:'video-twitter',
                //         component: () => import('@/views/Video/Twitter/index.vue'),
                //         meta:{
                //             title:'推特',
                //         }
                //     },{
                //         path:'/video/pipixia',
                //         name:'video-pipixia',
                //         component: () => import('@/views/Video/Pipixia/index.vue'),
                //         meta:{
                //             title:'皮皮虾',
                //         }
                //     }
                // ],
                meta:{
                    title:'视频',
                    menu: true,
                    keepAlive: true
                }
            },
            {
                path:'/player',
                name:'player',
                component:() => import('@/views/Player/index.vue'),
                meta:{
                    title:'播放器',
                    menu: false,
                    keepAlive: true
                }
            },
            {
                path:'/downloader',
                name:'downloader',
                component: () => import('@/views/Downloader/index.vue'),
                meta:{
                    title:'下载',
                    menu: true
                },
            },
            {
                path:'/settings',
                name:'settings',
                component: () => import('@/views/Settings/index.vue'),
                meta:{
                    title:'设置',
                    menu: true,
                    keepAlive: true
                },
            },
        ],
        meta:{
            menu: false
        },
    },
    {
        path:'/',
        redirect:'/home',
        meta:{
            title:'/',
            menu: false
        }
    }
]

const router = createRouter({
    history:createWebHashHistory(),
    routes
})

export default router