import {BootstrapVue, BootstrapVueIcons} from 'bootstrap-vue'

<template>
  <div id="app">
    <!--Navbar -->
    <b-navbar sticky toggleable="lg" type="light" variant="light">
      <b-navbar-brand id="logoNavbar" href="#" @click="onHome()">
        <img style="max-width: 150px" :src="require('../assets/logo.svg')">
      </b-navbar-brand>
      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav>
          <b-nav-item id="homeNavbarButton" @click="onHome()">Home</b-nav-item>
          <b-nav-item id="jobPostingsNavbarButton" active>Job postings</b-nav-item>
          <b-nav-item id="companiesNavbarButton" @click="onCompanies()">Companies</b-nav-item>
          <b-nav-item id="aboutUsNavbarButton" @click="onAboutUs()">About Us</b-nav-item>
        </b-navbar-nav>

        <b-navbar-nav v-if="!logged" class="ml-auto">
          <b-nav-item id="logInNavbarButton" @click="onLogIn()">Log in</b-nav-item>
        </b-navbar-nav>

        <b-navbar-nav v-if="logged" class="ml-auto">
          <b-nav-item id="profileNavbarButton" @click="onProfile()">{{ this.username }}</b-nav-item>
          <button id="logOutNavbarButton" class="btn btn-outline-danger" @click="onLogOut()"> Log Out </button>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
    <!--/.Navbar -->
    <!-- Job offers company view -->
    <div class="mx-1" id="jobPostingsView" v-show="!this.jobOfferView">
      <h2 class="title-offer"> {{ message }} </h2>
      <b-link v-if="is_company" id="showJobOfferModal" class="add-offer" v-b-modal.job-offer-modal>
        <b-icon icon="patch-plus" font-scale="2"></b-icon>
      </b-link>
      <b-container fluid id="searchContainer"  style="padding: 20px; align-self: center;
                                                font-family:'Work Sans SemiBold', Montserrat, sans-serif">
        <b-row align-h="center" id="searchTitleRow" class="mb-1">
          <p class="text-center" style="font-size: 22px">Find your perfect job!</p>
        </b-row>
        <b-row align-h="center" id="searchContentRow" class="mb-2" style="font-family:'Work Sans', sans-serif">
          <b-row id="searchSearchbarRow">
            <b-input id="searchbar" type="text" length=60 v-model="search"
                     placeholder="Search job offer...   "
                     style="border-radius: 0 !important" />
          </b-row>
          <b-row id="searchFiltersRow">
            <b-dropdown id="filterJobTypeDropdown" variant="light" class="ml-4" text="Job type" checkbox-menu allow-focus>
            <template #button-content>
             <span>
               Job type <font-awesome-icon size="1x" :icon="['fas', 'filter']" />
             </span>
            </template>
            <b-dropdown-form style="font-family: 'Work Sans',sans-serif">
              <b-form-checkbox v-model="checkedFullTime" id="checkboxFullTime" name="checkbox-full-time">
                Full-time
              </b-form-checkbox>
              <b-form-checkbox v-model="checkedPartTime" id="checkboxPartTime" name="checkbox-part-time">
                Part-time
              </b-form-checkbox>
              <b-form-checkbox v-model="checkedInternship" id="checkboxInternship" name="checkbox-internship">
                Internship
              </b-form-checkbox>
              <b-form-checkbox v-model="checkedFreelance" id="checkboxFreelance" name="checkbox-freelance">
                Freelance
              </b-form-checkbox>
              <b-form-checkbox v-model="checkedOther" id="checkboxOther" name="checkbox-other">
                Other
              </b-form-checkbox>
            </b-dropdown-form>
          </b-dropdown>
              <b-button id="searchButton" variant="warning" :disabled="!(checkedFullTime||checkedPartTime||checkedInternship
            ||checkedFreelance||checkedOther)" @click="searchJobOffers">
                Search!
              </b-button>
          </b-row>
        </b-row>
      </b-container>
      <b-container fluid v-if="notFound" id="notFoundContainer">
        <h2 class="not-found-message" id="notFoundMessage"> {{ notFoundMessage }} </h2>
      </b-container>
      <job-postings-view
        v-bind:job_offers = "job_offers"
        v-bind:companies_logos = "companies_logos"
        :key = "loaded_logos"
      ></job-postings-view>
      <b-modal ref="jobOfferModal"
               id="job-offer-modal"
               title="Post a job offer"
               hide-footer
      >
        <validation-observer ref="observer" v-slot="{ handleSubmit }">
          <b-form style="font-family:'Work Sans'" @submit.prevent="handleSubmit(onSubmitNewOffer)">
            <ValidationProvider name="JobName"  rules="alpha_spaces|required:true|max: 50" v-slot="validationContext">
              <b-form-group id="input-group-1" label="Job name" label-for="input-1">
                <b-form-input id="jobNameInput" v-model="jobOfferForm.jobName" placeholder="" type="text" :state="getValidationState(validationContext)"
                              aria-describedby="input-1-live-feedback"></b-form-input>
                <b-form-invalid-feedback id="input-1-live-feedback">{{ validationContext.errors[0] }}</b-form-invalid-feedback>
              </b-form-group>
            </ValidationProvider>

              <b-form-group id="input-group-3" label="Salary" label-for="input-3">
                <b-form-row>
                  <b-col ><b-form-input id="salaryInput" v-model="jobOfferForm.salary" type="number" min=0 max="9999999999999"/></b-col>
                  <b-col>
                    <b-form-select id="salaryTypeInput" v-model="jobOfferForm.salary_type"  :options="optionsSalaryType" placeholder="" type="text"></b-form-select>
                  </b-col>
                </b-form-row>
              </b-form-group>

            <validation-provider name="Location"  rules="required:true|max: 40" v-slot="validationContext">
              <b-form-group id="input-group-1" label="Location" label-for="input-1">
                <b-form-input id="locationInput" v-model="jobOfferForm.location" placeholder="e.g. 'Barcelona', 'Remote'" type="text" :state="getValidationState(validationContext)"
                              aria-describedby="input-1-live-feedback"></b-form-input>
                <b-form-invalid-feedback id="input-1-live-feedback">{{ validationContext.errors[0] }}</b-form-invalid-feedback>
              </b-form-group>
            </validation-provider>

            <validation-provider name="ContractType"  :rules="{ max: 500}" v-slot="validationContext">
              <b-form-group id="input-group-2" label="Contract type" label-for="input-2">
                <b-form-select id="contractTypeInput" v-model="jobOfferForm.contractType" :options="optionsContractType" placeholder="" type="text" :state="getValidationState(validationContext)"
                               aria-describedby="input-2-live-feedback"></b-form-select>
                <b-form-invalid-feedback id="input-2-live-feedback">{{ validationContext.errors[0] }}</b-form-invalid-feedback>
              </b-form-group>
            </validation-provider>

            <validation-provider name="WorkingHours"  rules="numeric|max:60" v-slot="validationContext">
              <b-form-group id="input-group-3" label="Weekly working hours" label-for="input-3">
                <b-form-input id="workingHoursInput" v-model="jobOfferForm.workingHours" placeholder="" type="number" min=0 max=168 :state="getValidationState(validationContext)"
                              aria-describedby="input-3-live-feedback"></b-form-input>
                <b-form-invalid-feedback id="input-3-live-feedback">{{ validationContext.errors[0] }}</b-form-invalid-feedback>
              </b-form-group>
            </validation-provider>

            <validation-provider name="Description"  :rules="{ max: 3000}" v-slot="validationContext">
              <b-form-group id="input-group-2" label="Description" label-for="input-2">
                <b-form-textarea id="descriptionInput" v-model="jobOfferForm.description" :state="getValidationState(validationContext)"
                                 aria-describedby="input-2-live-feedback"  rows="5"
                                 placeholder="(Optional) Description of the job, requirements, job benefits, etc."></b-form-textarea>
                <b-form-invalid-feedback id="input-2-live-feedback">{{ validationContext.errors[0] }}</b-form-invalid-feedback>
              </b-form-group>
            </validation-provider>

            <div class="d-grid gap-2 d-md-flex justify-content-md-end">
              <button id="postJobOfferButton" class="btn btn-warning justify-content-md-end">Post Job Offer!</button>
            </div>
          </b-form>
        </validation-observer>
      </b-modal>
    </div>
    <!-- /Job offers company view -->
  </div>
</template>

<script>
import Vue from 'vue'
import axios from 'axios'
import {mapState} from 'vuex'
import firebase from 'firebase/compat'

export default {
  data () {
    return {
      message: 'Job Postings',
      logged: false,
      job_offers: [], // {'id': 0, 'jobName': 'Waiter', 'company': 'Terra Restaurant', 'description': 'This offer is fake and it will be deleted in the next update', 'type': 'Part time'}, {'id': 1, 'jobName': 'Journalist', 'company': 'The Sun', 'description': 'This offer is fake and it will be deleted in the next update', 'type': 'Part time'}],
      username: '',
      token: '',
      is_jobseeker: true,
      is_company: false,
      is_admin: false,
      jobOfferForm: {
        jobName: '',
        description: '',
        salary: '',
        salary_type: '',
        location: '',
        contractType: '',
        workingHours: ''
      },
      optionsContractType: ['Full-time', 'Part-time', 'Internship', 'Freelance', 'Other'],
      optionsSalaryType: ['Hour', 'Month', 'Year'],
      companies_logos: {},
      selected: [],
      search: '',
      checkedFullTime: true,
      checkedPartTime: true,
      checkedInternship: true,
      checkedFreelance: true,
      checkedOther: true,
      options: [
        { item: 'Full-time', name: 'Full-time' },
        { item: 'Part-time', name: 'Part-time' },
        { item: 'Internship', name: 'Internship' },
        { item: 'Freelance', name: 'Freelance' },
        { item: 'Other', name: 'Other' }
      ],
      notFound: false,
      notFoundMessage: 'Oops, we did not find any job offer matching your search...',
      loaded_logos: 0
    }
  },
  methods: {
    onHome () {
      this.$router.push('/')
    },
    getValidationState ({ dirty, validated, valid = null }) {
      return dirty || validated ? valid : null
    },
    onProfile () {
      if (this.is_jobseeker && this.logged) {
        this.$router.push('/job_seeker/' + this.username)
      } else if (this.is_company && this.logged) {
        this.$router.push('/company/' + this.username)
      }
    },
    onLogIn () {
      this.$router.push('/login')
    },
    onCompanies () {
      this.$router.push({ path: '/companies' })
    },
    onLogOut () {
      this.$store.commit('logout')
      this.$router.push('/')
    },
    onAboutUs () {
      this.$router.push('/about_us')
    },
    onJobOffer (id) {
      this.$router.push('/job_posting/' + id)
    },
    getJobOffers () {
      const path = Vue.prototype.$API_BASE_URL + 'offers'
      axios.get(path)
        .then((res) => {
          this.job_offers = []
          for (var jobOffer in res.data.OfferList) {
            jobOffer = res.data.OfferList[jobOffer]
            jobOffer.publication_date = jobOffer.publication_date.split('T')[0]
            this.job_offers.push(jobOffer)
          }
          this.getCompaniesLogos()
          if (this.job_offers.length > 0) {
            this.notFound = false
          } else {
            this.notFound = true
            this.notFoundMessage = 'Oops, actually we do not have any job offer...'
          }
        })
        .catch((error) => {
          console.error(error)
        })
    },
    searchJobOffers () {
      const path = Vue.prototype.$API_BASE_URL + 'offers'
      let searchParams = {}
      const noFilters = this.checkedFullTime && this.checkedPartTime && this.checkedInternship && this.checkedFreelance && this.checkedOther
      if ((this.search === '') && noFilters) {
        searchParams = {params: {}}
      } else if ((this.search !== '') && noFilters) {
        searchParams = {params: {'keyword': this.search}}
      } else {
        let checkedFilters = ''
        if (this.checkedFullTime) { checkedFilters += 'Full-time,' }
        if (this.checkedPartTime) { checkedFilters += 'Part-time,' }
        if (this.checkedInternship) { checkedFilters += 'Internship,' }
        if (this.checkedFreelance) { checkedFilters += 'Freelance,' }
        if (this.checkedOther) { checkedFilters += 'Other' }
        if (this.search !== '') {
          searchParams = {params: {'keyword': this.search, 'job_type': checkedFilters}}
        } else {
          searchParams = {params: {'job_type': checkedFilters}}
        }
      }

      axios.get(path, searchParams)
        .then((res) => {
          this.job_offers = []
          for (var jobOffer in res.data.OfferList) {
            jobOffer = res.data.OfferList[jobOffer]
            jobOffer.publication_date = jobOffer.publication_date.split('T')[0]
            this.job_offers.push(jobOffer)
          }
          this.getCompaniesLogos()
          if (this.job_offers.length > 0) {
            this.notFound = false
          } else {
            this.notFound = true
            this.notFoundMessage = 'Oops, we did not find any job offer matching your search...'
          }
        })
        .catch((error) => {
          console.error(error)
        })
    },
    getCompaniesLogos () {
      this.loaded_logos = 0
      for (let o in this.job_offers) {
        let offer = this.job_offers[o]
        this.companies_logos[offer.company] = null
        firebase.storage().ref(`images/${offer.company}/avatar`).getDownloadURL()
          .then((url) => {
            this.companies_logos[offer.company] = url
            this.loaded_logos += 1
          })
          .catch(() => {
            console.log('This avatar does not exist')
          })
      }
    },
    onSubmitNewOffer () {
      const path = Vue.prototype.$API_BASE_URL + 'job_offer/' + this.username
      var values = {
        job_name: this.jobOfferForm.jobName,
        description: this.jobOfferForm.description,
        location: this.jobOfferForm.location
      }
      if (this.jobOfferForm.contractType !== '' && this.jobOfferForm.contractType !== null) {
        values.contract_type = this.jobOfferForm.contractType
      }
      if (this.jobOfferForm.salary !== '' && this.jobOfferForm.salary !== null && this.jobOfferForm.salary_type !== '' && this.jobOfferForm.salary_type !== null) {
        values.salary = this.jobOfferForm.salary + '€/' + this.jobOfferForm.salary_type
      }
      if (!isNaN(this.jobOfferForm.workingHours) && this.jobOfferForm.workingHours !== '') {
        values.working_hours = this.jobOfferForm.workingHours
      }
      console.log(values)
      axios.post(path, values, {
        auth: {username: this.token}})
        .then((res) => {
          this.showToastSubmitNewOffer()
          this.getJobOffers()
        })
        .catch((error) => {
          console.error(error)
          this.showToastSubmitNewOfferError()
        })
      this.$bvModal.hide('job-offer-modal')
      this.onReset()
    },
    showToastSubmitNewOffer () {
      /* eslint-disable */
      this.$bvToast.toast('Job Offer correctly posted', {
        title: `Information`,
        variant: 'success',
        solid: true
      })
    },
    showToastSubmitNewOfferError (error) {
      /* eslint-disable */
      this.$bvToast.toast('Error while trying to submit offer ', {
        title: `Warning`,
        variant: 'danger',
        solid: true
      })
    },
    initJobOfferForm () {
      this.jobOfferForm.jobName = ''
      this.jobOfferForm.description = ''
      this.jobOfferForm.salary = ''
      this.jobOfferForm.salary_type = ''
      this.jobOfferForm.vacancyNumber = ''
      this.jobOfferForm.location = ''
      this.jobOfferForm.contractType = ''
      this.jobOfferForm.workingHours = ''
      this.jobOfferForm.minimumExperience = ''
    },
    onReset () {
      this.initJobOfferForm()
    }
  },
  created () {
    this.logged = this.$store.state.logged
    this.username = this.$store.state.username
    this.is_jobseeker = this.$store.state.isJobSeeker
    this.is_company = this.$store.state.isCompany
    this.token = this.$store.state.token
    this.is_admin = this.$store.state.isAdmin
    this.getJobOffers()
  },
  computed: mapState({
    token: state => state.token,
    logged: state => state.logged,
    username: state => state.username,
    isJobSeeker: state => state.isJobSeeker,
    isCompany: state => state.isCompany,
    isAdmin: state => state.isAdmin
  })
}
</script>

<style>
.navbar.navbar-light{
  font-family: "Work Sans SemiBold", Montserrat, sans-serif;
  font-size: 18px;
  padding: 20px;
  margin-bottom: 20px;
}
.custom-control-label:after{
  background-color:#ffc106;
}
.companyNameJobOfferCard{
  font-family: "Work Sans SemiBold", Montserrat, sans-serif;
  font-size: 18px;
  margin-bottom: 0.3rem;
}
.titleJobOfferCard{
  font-family: "Work Sans SemiBold", Montserrat, sans-serif;
  font-weight: bold;
  font-size: 24px;
  margin-bottom: 0;
}
.not-found-message{
  font-family: "Work Sans SemiBold", Montserrat, sans-serif;
  font-size: 22px;
  padding: 50px;
}
</style>
