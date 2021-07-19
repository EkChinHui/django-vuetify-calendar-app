<template>
  <div class="d-flex flex-column justify-center">
    <h1 class="text-center ma-10">Calendar</h1>
    <v-sheet tile height="54" class="d-flex">
      <v-btn class="ml-4" color="primary" @click.stop="dialog = true">
        New Event
      </v-btn>
      <v-btn outlined class="mr-4 ml-4" color="grey darken-2" @click="setToday">
        Today
      </v-btn>

      <v-btn icon class="ml-2" @click="$refs.calendar.prev()">
        <v-icon>mdi-chevron-left</v-icon>
      </v-btn>

      <v-toolbar-title v-if="$refs.calendar" class="text-center">
        {{ $refs.calendar.title }}
      </v-toolbar-title>

      <v-btn icon class="ml-2" @click="$refs.calendar.next()">
        <v-icon>mdi-chevron-right</v-icon>
      </v-btn>
    </v-sheet>

    <v-dialog
      v-model="dialog"
      max-width="300"
      transition="dialog-bottom-transition"
    >
      <v-card>
        <v-container>
          <v-form @submit.prevent="submitForm">
            <v-layout col wrap>
              <v-text-field
                v-model="eventForm.name"
                type="text"
                label="Name"
              ></v-text-field>
              <v-text-field
                v-model="eventForm.description"
                type="message"
                label="Description"
              ></v-text-field>
              <v-menu
                ref="startmenu"
                v-model="startmenu"
                :close-on-content-click="false"
                :return-value.sync="eventForm.start"
                transition="scale-transition"
                offset-y
                min-width="auto"
              >
                <template v-slot:activator="{ on, attrs }">
                  <v-combobox
                    v-model="eventForm.start"
                    chips
                    small-chips
                    label="Start date"
                    prepend-icon="mdi-calendar"
                    readonly
                    v-bind="attrs"
                    v-on="on"
                  ></v-combobox>
                </template>
                <v-date-picker v-model="eventForm.start" no-title scrollable>
                  <v-spacer></v-spacer>
                  <v-btn text color="primary" @click="startmenu = false">
                    Cancel
                  </v-btn>
                  <v-btn
                    text
                    color="primary"
                    @click="$refs.startmenu.save(eventForm.start)"
                  >
                    OK
                  </v-btn>
                </v-date-picker>
              </v-menu>

              <v-menu
                ref="endmenu"
                v-model="endmenu"
                :close-on-content-click="false"
                :return-value.sync="eventForm.end"
                transition="scale-transition"
                offset-y
                min-width="auto"
              >
                <template v-slot:activator="{ on, attrs }">
                  <v-combobox
                    v-model="eventForm.end"
                    chips
                    small-chips
                    label="End date (optional)"
                    prepend-icon="mdi-calendar"
                    readonly
                    v-bind="attrs"
                    v-on="on"
                  ></v-combobox>
                </template>
                <v-date-picker v-model="eventForm.end" no-title scrollable>
                  <v-spacer></v-spacer>
                  <v-btn text color="primary" @click="endmenu = false">
                    Cancel
                  </v-btn>
                  <v-btn
                    text
                    color="primary"
                    @click="$refs.endmenu.save(eventForm.end)"
                  >
                    OK
                  </v-btn>
                </v-date-picker>
              </v-menu>
              <v-btn type="submit" color="primary" @click.stop="dialog = false"
                >Create Event</v-btn
              >
            </v-layout>
          </v-form>
        </v-container>
      </v-card>
    </v-dialog>

    <v-sheet height="600">
      <v-calendar
        ref="calendar"
        v-model="focus"
        :type="type"
        :events="events"
        :event-overlap-threshold="30"
        :event-color="getEventColor"
        @change="getEvents"
        @click:event="showEvent"
      ></v-calendar>
      <v-menu
        v-model="selectedOpen"
        :close-on-content-click="false"
        :activator="selectedElement"
        offset-x
        max-width="400"
      >
        <v-card color="grey lighten-4" min-width="350px" flat>
          <v-toolbar :color="selectedEvent.color" dark>
            <v-toolbar-title v-html="selectedEvent.name"></v-toolbar-title>
            <v-spacer></v-spacer>
          </v-toolbar>
          <v-card-text v-text="selectedEvent.description">
          <v-spacer></v-spacer>
          </v-card-text>
          <v-card-actions class="d-flex justify-space-around">
            <v-btn text color="secondary" @click="selectedOpen = false">
              Cancel
            </v-btn>
            <v-btn text color="red" @click="removeEvent"> Remove </v-btn>
          </v-card-actions>
        </v-card>
      </v-menu>
    </v-sheet>
    <v-alert
      max-width="500"
      type="error"
      outlined
      transition="slide-y-transition"
      class="text-cennter align-self-center"
      :value="openAlert"
      >{{ alert }}
    </v-alert>
  </div>
</template>




<script>
import axios from "axios";
import { isAfter, isSameDay, parseISO } from "date-fns";

export default {
  data: () => ({
    focus: "",
    type: "month",
    value: "",
    menu: false,
    events: [],
    selectedElement: null,
    selectedEvent: {},
    selectedOpen: false,
    dialog: false,
    startmenu: "",
    endmenu: "",
    openAlert: false,
    alert: "",
    eventForm: {
      name: "",
      description: "",
      start: "",
      end: "",
    },
  }),
  mounted() {
    this.getEvents();
    axios.defaults.xsrfHeaderName = 'X-CSRFToken'
    axios.defaults.xsrfCookieName = 'csrftoken'
  },
  methods: {
    getEvents() {
      const events = [];
      let data = {};
      let event = null;
      axios.get("/api/event-list/", { headers: {} }).then((res) => {
        data = res.data;
        for (let i = 0; i < data.length; i++) {
          event = data[i];

          events.push({
            id: event["id"],
            name: event["name"],
            description: event["description"],
            start: event["start"],
            end: event["end"],
            color: "blue",
            timed: false,
          });
        }
      });
      this.events = events;
    },
    getEventColor(event) {
      return event.color;
    },
    rnd(a, b) {
      return Math.floor((b - a + 1) * Math.random()) + a;
    },
    setToday() {
      this.focus = "";
    },
    submitForm() {
      let data = this.validateForm();
      if (!data) {
        return;
      }
      console.log(data)
      axios
        .post("/api/event-create/", data, {
          headers: {}
        })
        .then((res) => {
          console.log(res);
          this.getEvents();
        });
      // clear fields
      this.eventForm.name = "";
      this.eventForm.description = "";
      this.eventForm.start = "";
      this.eventForm.end = "";
    },
    showEvent({ nativeEvent, event }) {
      const open = () => {
        this.selectedEvent = event;
        this.selectedElement = nativeEvent.target;
        requestAnimationFrame(() =>
          requestAnimationFrame(() => (this.selectedOpen = true))
        );
      };

      if (this.selectedOpen) {
        this.selectedOpen = false;
        requestAnimationFrame(() => requestAnimationFrame(() => open()));
      } else {
        open();
      }

      nativeEvent.stopPropagation();
    },
    removeEvent() {
      axios
        .delete(
          "/api/event-delete/"+this.selectedEvent.id+"/",
          { data: JSON.stringify(this.selectedEvent) },
          {
            headers: {},
          }
        )
        .then((res) => {
          console.log(res);
          this.selectedOpen = false;
          this.getEvents();
        });
    },
    validateForm() {
      // check for required fields
      let name = this.eventForm.name
      let start = this.eventForm.start
      let end = this.eventForm.end

      if (name && start) {
        end = !end ? start : end;
        if (!this.areDatesValid(start, end)) {
          // trigger end date error
          this.displayAlert("Start Date has to be before or same as End Date");
          return;
        }
        return {
          name: name,
          description: this.eventForm.description,
          start: start,
          end: end,
        };
      } else {
        // trigger required field error
        this.displayAlert("Name and Start Date are required");
      }
    },
    areDatesValid(start, end) {
      let startDate = parseISO(start)
      let endDate = parseISO(end)
      return isAfter(endDate, startDate) || isSameDay(startDate, endDate);
    },
    displayAlert(message) {
      this.alert = message;
      this.openAlert = true;
      setTimeout(() => {
        this.openAlert = false;
      }, 3000);
      setTimeout(() => {
        this.alert = "";
      }, 3500);
    },
  },
};
</script>


<style scoped>
</style>
