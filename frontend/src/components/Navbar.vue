<template>

        <nav class="navbar navbar-expand navbar-dark bg-dark">
            <div class="container-fluid">
                <a class="navbar-brand" href="#"> 
                    <router-link :to=" {name:'Home'} " class="logo-link">PK SPOT MAP</router-link>
                </a>

                <div class="collapse navbar-collapse" id="navbarMenu">

                    <ul class="navbar-nav ms-auto">
                        <li class="nav-item">
                            <router-link :to=" {name:'Login'} " class="nav-link">Login</router-link>
                        </li>
                        <li class="nav-item">
                            <router-link :to=" {name:'SignUp'} " class="nav-link">Sign Up</router-link>
                        </li>
                    </ul>

                </div>
            </div>
        </nav>

</template>


<style scoped>

.logo-link {
    color: white;
    text-decoration: none;
}

</style>