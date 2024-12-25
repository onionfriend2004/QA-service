const centrifuge = new Centrifuge("{{ ws_url }}", {
    token: "{{ token }}"
});
const sub = centrifuge.newSubscription('room:{{ question.id }}');
sub.on('publication', function(ctx) {
    console.log(ctx.data);
})
sub.subscribe();
centrifuge.connect();