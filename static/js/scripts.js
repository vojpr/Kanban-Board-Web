// Insert username into hero headline
$(".nameinput").on("input", function () {
  $("#target").html("Hello " + $(this).val());
});

// Change navbar color on scroll
$(function () {
  $(document).scroll(function () {
    var $nav = $(".navbar-fixed-top");
    $nav.toggleClass("scrolled", $(this).scrollTop() > 20);
  });
});

// Drag and drop
$(function () {
  $("#to-do-cards, #in-progress-cards, #done-cards")
    .sortable({
      opacity: 0.91,
      revert: 200,
      connectWith: ".sortable-cards",
      update: function () {
        reorderTasks();
      },
    })
    .disableSelection();
});

// Create Task (and write to the database)
$("form#create-task").submit(function () {
  var taskInput = $('input[name="new-task"]').val().trim();
  if (taskInput) {
    $.ajax({
      url: "/create/",
      data: {
        "new-task": taskInput,
      },
      dataType: "json",
      success: function (data) {
        if (data.task) {
          appendToKanban(data.task);
        }
      },
    });
  }
  $("form#create-task").trigger("reset");
  return false;
});
function appendToKanban(task) {
  $("#to-do-cards").prepend(`
        <div id="task-${task.pk}" data-pk="${task.pk}" class="task-container">
            <div class="task-text-div">
                <p class="task-text">${task.text}</p>
            </div>
            <div class="delete-div">
                <button onClick="deleteTask(${task.pk})" class="task-button"><i class="uil uil-times"></i></button>
            </div>
        </div>
    `);
}

// Delete Task (and delete from the database)
function deleteTask(pk) {
  $.ajax({
    url: "/delete/",
    data: {
      pk: pk,
    },
    dataType: "json",
    success: function (data) {
      if (data.deleted) {
        $("#task-" + pk).remove();
      }
    },
  });
}

// Re-write sorted tasks in the database
function reorderTasks() {
  sort = [];
  $(".sortable-cards")
    .children()
    .each(function () {
      sort.push({
        pk: $(this).data("pk"),
        order: $(this).index(),
        column_name: $(this).parent().data("column"),
      });
    });
  $.ajax({
    url: "/reorder/",
    data: {
      sort: JSON.stringify(sort),
    },
    datatype: "json",
  });
}
