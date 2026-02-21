<script>
	import { Checkbox } from "$lib/components/ui/checkbox/index.js";
	let {
		checked = false,
		onCheckedChange = (v) => (checked = v),
		...restProps
	} = $props();
</script>

<div class="flex items-center justify-center">
	<Checkbox bind:checked={() => checked, onCheckedChange} {...restProps} />
</div>