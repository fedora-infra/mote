function calcCalHeight(){
	var newHeight;
	if(window.innerWidth<=580){
          newHeight = window.innerHeight-250;
	} else if(window.innerWidth<=896) {
          newHeight = window.innerHeight-220;
	} else if(window.innerWidth<=991) {
          newHeight = window.innerHeight-188;
	} else {
          newHeight = window.innerHeight-180;
	}
	return newHeight;

}

document.addEventListener('DOMContentLoaded', async function() {
  var calendarEl = document.getElementById('calendar');

  var calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: 'dayGridWeek',
    handleWindowResize: true,
    windowResize: function(arg) {
        calendar.setOption('height', calcCalHeight());
    },
    fixedWeekCount:false,
    height: calcCalHeight(),
    headerToolbar: false,

    loading: function(isLoading) {
      if(isLoading){
        $("#spin").removeClass("fa-calendar").addClass("spinner-border");
      } else {
        $("#spin").removeClass("spinner-border").addClass("fa-calendar");
      }
    },

    views: {
      dayGridMonth: {
        dayMaxEventRows: true,
        dayMaxEvents: true,
        showNonCurrentDates: true,
        displayEventTime: false,
        validRange: function(now) {
          return {
            end: new Date(now.getFullYear(), now.getMonth()+1, 0),
          };
        },
        dateClick: function(info) {
  	calendar.changeView('dayGridDay', info.dateStr);
          $("#month").removeClass("active");
          $("#week").removeClass("active");
          $("#day").addClass("active");
        },
      },

      dayGridWeek: {
        dayMaxEventRows: true,
        displayEventTime: false,
         eventContent: function(arg) {
  	 console.log(arg);
           let el = document.createElement('div');
  	 el.className = "fc-event-main-body";
  	 el.innerHTML = 
  	     `<div class="fc-event-title">`+ arg.event.title +`</div>
  	      <div class="fc-event-text">
                  `+ arg.event.extendedProps.attendees +` peoples | `+ arg.event.extendedProps.topics +` topics
  	      </div>`;
           return {domNodes: [ el ]}
         },
        dayHeaderContent: function(arg) {
        
          let weekday = arg.date.toLocaleDateString('en-US', {weekday: 'short'});
          let day = arg.date.toLocaleDateString('en-US', {day: 'numeric'});
        
          return { html: weekday + "<br /><b>" + day + "</b>" };
        },
        validRange: function(now) {
          return {
            end: now,
          };
        },
      },

      dayGridDay: {
        dayHeaderFormat: { weekday: 'long', day: 'numeric', month: "long" }  ,
        validRange: function(now) {
          return {
            end: now,
          };
        },
        eventContent: function(arg) {
          console.log(arg);
          let el = document.createElement('div');
          el.className = "fc-event-main-body";
          el.innerHTML = 
              `<div class="fc-event-title">`+ arg.event.title +`</div>
               <div class="fc-event-text">
                 `+ arg.event.extendedProps.attendees +` peoples | `+ arg.event.extendedProps.topics +` topics
               </div>`;
          return {domNodes: [ el ]}
        },
      },
    },
    eventTimeFormat: { // like '14:30'
      hour: '2-digit',
      minute: '2-digit',
      hour12: false,
      omitZeroMinute: false,
    },
    defaultTimedEventDuration: '02:00',
    nextDayThreshold: '02:00:00',
    events: "/cal/events",
    eventClick: function(info) {
      // info.event.title
      info.jsEvent.preventDefault();
      $('#evt-smry .modal-content').load('/smry/'+info.event.url,function(){
        var modal = new bootstrap.Modal(document.getElementById('evt-smry'));
        modal.show();
      });
    }
  });

  $("#curDate").text(calendar.getDate().toLocaleDateString('en-US', {month: 'long', year: 'numeric'}));
  calendar.render();

  document.getElementById('month').addEventListener('click', function() {
    calendar.changeView('dayGridMonth'); // call method
    $("#week").removeClass("active");
    $("#day").removeClass("active");
    $("#month").addClass("active");
  });

  document.getElementById('week').addEventListener('click', function() {
    calendar.changeView('dayGridWeek'); // call method
    $("#month").removeClass("active");
    $("#day").removeClass("active");
    $("#week").addClass("active");
  });

  document.getElementById('day').addEventListener('click', function() {
    calendar.changeView('dayGridDay'); // call method
    $("#month").removeClass("active");
    $("#week").removeClass("active");
    $("#day").addClass("active");
  });

  document.getElementById('prev').addEventListener('click', function() {
    calendar.prev();
    $("#curDate").text(calendar.getDate().toLocaleDateString('en-US', {month: 'long', year: 'numeric'}));
  });

  document.getElementById('next').addEventListener('click', function() {
    calendar.next();
    $("#curDate").text(calendar.getDate().toLocaleDateString('en-US', {month: 'long', year: 'numeric'}));
  });

  document.getElementById('today').addEventListener('click', function() {
    calendar.today();
    $("#curDate").text(calendar.getDate().toLocaleDateString('en-US', {month: 'long', year: 'numeric'}));
  });
});
