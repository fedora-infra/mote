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
  function swMonthView(){
    calendar.changeView('dayGridMonth');
    $("#curDate").text(calendar.view.title);
    $("#week").removeClass("active");
    $("#day").removeClass("active");
    $("#month").addClass("active");
  }
  function swWeekView(){
    calendar.changeView('dayGridWeek');
    $("#curDate").text(calendar.view.title);
    $("#month").removeClass("active");
    $("#day").removeClass("active");
    $("#week").addClass("active");
  }
  function swDayView(date=none){
    calendar.changeView('dayGridDay', date);
    $("#curDate").text(calendar.view.title);
    $("#month").removeClass("active");
    $("#week").removeClass("active");
    $("#day").addClass("active");
  }

  function eventDetailsHTML(arg){
    let el = document.createElement('div');
    el.className = "fc-event-main-body";
    el.innerHTML = 
        `<div class="fc-event-title">`+ arg.event.title +`</div>
         <div class="fc-event-text">
             `+ arg.event.extendedProps.attendees +` peoples | `+ arg.event.extendedProps.topics +` topics
         </div>`;
    return {domNodes: [ el ]}
  }
  function eventExtDetailsHTML(arg){
    let el = document.createElement('div');
    el.className = "fc-event-main-body";
    el.innerHTML = 
        `<div class="fc-event-title">`+ arg.event.title +`</div>
         <div class="fc-event-text">
	   <span class="pe-2"><i class="fas fa-clock fa-lg me-2"></i>`+ arg.event.extendedProps.length +` min</span> 
	   <span class="pe-2"><i class="fas fa-users fa-lg me-2"></i>`+ arg.event.extendedProps.attendees +` peoples</span> 
           <span><i class="fas fa-comments fa-lg me-2"></i>`+ arg.event.extendedProps.topics +` topics</span>
         </div>`;
    return {domNodes: [ el ]}
  }

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

    moreLinkClick: function(info) {
      swDayView(info.date);
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
          swDayView(info.dateStr);
        },
      },

      dayGridWeek: {
        dayMaxEventRows: true,
        displayEventTime: false,
        eventContent: eventDetailsHTML,
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
        eventContent: eventExtDetailsHTML,
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
      $('#evt-smry .modal-content').load('/smry/'+info.event.url.replace(/^\//, ''), function(responseText, textStatus, jqXHR){
	if(textStatus == "success"){
          var modal = new bootstrap.Modal(document.getElementById('evt-smry'));
          modal.show();
	}
      });
    }
  });

  $("#curDate").text(calendar.view.title);
  // $("#curDate").text(calendar.getDate().toLocaleDateString('en-US', {month: 'long', year: 'numeric'}));
  calendar.render();

  document.getElementById('month').addEventListener('click', swMonthView);
  document.getElementById('week').addEventListener('click', swWeekView);
  document.getElementById('day').addEventListener('click', swDayView);

  document.getElementById('prev').addEventListener('click', function() {
    calendar.prev();
    $("#curDate").text(calendar.view.title);
    // $("#curDate").text(calendar.getDate().toLocaleDateString('en-US', {month: 'long', year: 'numeric'}));
  });

  document.getElementById('next').addEventListener('click', function() {
    calendar.next();
    $("#curDate").text(calendar.view.title);
    // $("#curDate").text(calendar.getDate().toLocaleDateString('en-US', {month: 'long', year: 'numeric'}));
  });

  document.getElementById('today').addEventListener('click', function() {
    calendar.today();
    $("#curDate").text(calendar.view.title);
    // $("#curDate").text(calendar.getDate().toLocaleDateString('en-US', {month: 'long', year: 'numeric'}));
  });
});
